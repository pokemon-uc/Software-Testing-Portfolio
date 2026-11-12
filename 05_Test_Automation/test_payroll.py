"""pytest tests for the payroll business logic (payroll.py).

Each test name starts with its Test Case ID from 02_Test_Case_Design.
Run:  pytest test_payroll.py -v
"""
import pytest

from payroll import (InvalidTransitionError, PayrollRun, ValidationError, compute_bonus, compute_payslip,
                     compute_professional_tax, compute_pf, validate_basic, validate_emp_id, validate_lop,
                     validate_name, validate_overtime)


# ======================= Equivalence Partitioning =======================

def test_TC_EP_02_invalid_employee_id_format():
    with pytest.raises(ValidationError):
        validate_emp_id("EMP12")


def test_TC_EP_03_name_with_digits_rejected():
    with pytest.raises(ValidationError):
        validate_name("Ravi123")


def test_TC_EP_04_name_with_only_spaces_rejected():
    with pytest.raises(ValidationError):
        validate_name("   ")


# ======================= Boundary Value Analysis =======================

# Basic salary: valid 10,000 - 5,00,000
@pytest.mark.parametrize("basic, valid", [
    pytest.param(9999, False, id="TC_BVA_01 basic=9999"),
    pytest.param(10000, True, id="TC_BVA_02 basic=10000"),
    pytest.param(500000, True, id="TC_BVA_03 basic=500000"),
    pytest.param(500001, False, id="TC_BVA_04 basic=500001"),
])
def test_basic_salary_boundaries(basic, valid):
    if valid:
        assert validate_basic(basic) == basic
    else:
        with pytest.raises(ValidationError):
            validate_basic(basic)


# Overtime hours: valid 0 - 60
def test_TC_BVA_05_overtime_60_hours_accepted():
    assert validate_overtime(60) == 60
    assert compute_payslip(20000, overtime_hours=60)["ot_pay"] == 12000


def test_TC_BVA_06_overtime_61_hours_rejected():
    with pytest.raises(ValidationError):
        validate_overtime(61)


# LOP days: valid 0 - 30
def test_TC_BVA_07_lop_30_days_accepted():
    assert compute_payslip(30000, lop_days=30)["lop_deduction"] == 30000


def test_TC_BVA_08_lop_31_days_rejected():
    with pytest.raises(ValidationError):
        validate_lop(31)


# PF: 12% of basic, basic counted only up to 15,000 (max PF 1,800)
def test_TC_BVA_09_pf_at_ceiling_15000():
    assert compute_pf(15000) == 1800


def test_TC_BVA_10_pf_above_ceiling_is_capped():
    assert compute_pf(20000) == 1800


# Professional tax: Rs 200 if gross >= 25,000
def test_TC_BVA_11_pt_when_gross_exactly_25000():
    assert compute_professional_tax(25000) == 200


def test_TC_BVA_12_no_pt_when_gross_24999():
    assert compute_professional_tax(24999) == 0


# ======================= Decision Table (Bonus) =======================

@pytest.mark.parametrize("emp_type, years, rating, expected", [
    pytest.param("Permanent", 3, 4, 2000, id="TC_DT_01 R1 Permanent, years>=1, rating>=4 -> 10%"),
    pytest.param("Permanent", 3, 3, 1000, id="TC_DT_02 R2 Permanent, years>=1, rating<4 -> 5%"),
    pytest.param("Permanent", 0, 5, 0, id="TC_DT_03 R3 Permanent, years<1, rating>=4 -> 0%"),
    pytest.param("Permanent", 0, 2, 0, id="TC_DT_04 R4 Permanent, years<1, rating<4 -> 0%"),
    pytest.param("Contract", 2, 5, 1000, id="TC_DT_05 R5 Contract, rating>=4 -> 5%"),
    pytest.param("Contract", 2, 3, 0, id="TC_DT_06 R6 Contract, rating<4 -> 0%"),
])
def test_bonus_decision_table(emp_type, years, rating, expected):
    assert compute_bonus(20000, emp_type, years, rating) == expected


# ======================= State Transition (Payroll Run) =======================

def test_TC_ST_01_draft_to_processed():
    run = PayrollRun("2026-11")
    assert run.apply("process") == "PROCESSED"


def test_TC_ST_02_full_path_to_paid():
    run = PayrollRun("2026-11")
    for event in ("process", "approve", "pay"):
        run.apply(event)
    assert run.state == "PAID"
    assert run.history == ["DRAFT", "PROCESSED", "APPROVED", "PAID"]


def test_TC_ST_03_rejected_run_revised_to_draft():
    run = PayrollRun("2026-11")
    run.apply("process")
    assert run.apply("reject") == "REJECTED"
    assert run.apply("revise") == "DRAFT"


def test_TC_ST_04_cannot_pay_a_draft_run():
    run = PayrollRun("2026-11")
    with pytest.raises(InvalidTransitionError):
        run.apply("pay")
    assert run.state == "DRAFT"


# TC_ST_05 (PAID -> revise) is tested through the UI in test_ui_selenium.py

def test_TC_ST_06_cannot_process_a_paid_run():
    run = PayrollRun("2026-11")
    for event in ("process", "approve", "pay"):
        run.apply(event)
    with pytest.raises(InvalidTransitionError):
        run.apply("process")


# ======================= Functional (full payslip) =======================

def test_TC_FN_04_payslip_permanent_basic_30000():
    slip = compute_payslip(30000, overtime_hours=10, lop_days=2, emp_type="Permanent",
                           years_of_service=3, rating=4)
    assert slip["gross"] == 45000      # 30000 + 12000 + 3000 + 2000 - 2000
    assert slip["bonus"] == 3000       # 10%
    assert slip["pf"] == 1800          # capped
    assert slip["professional_tax"] == 200
    assert slip["net"] == 46000        # 45000 + 3000 - 1800 - 200
