"""
Employee Payroll Management System - core business logic.

This is the System Under Test (SUT) for the Software Testing portfolio.
Business rules are specified in 01_Test_Plan/Test_Plan.md (Section 3).
"""
import re

# ---------------- Business constants ----------------
MIN_BASIC = 10_000
MAX_BASIC = 500_000
HRA_RATE = 0.40            # 40% of basic
DA_RATE = 0.10             # 10% of basic
OT_RATE_PER_HOUR = 200     # flat overtime rate (Rs/hour)
MAX_OT_HOURS = 60
MAX_LOP_DAYS = 30
DAYS_IN_MONTH = 30
PF_RATE = 0.12
PF_WAGE_CEILING = 15_000   # PF computed on basic up to this ceiling (max PF = 1800)
PT_THRESHOLD = 25_000      # Professional Tax applies when gross >= 25,000
PT_AMOUNT = 200
EMPLOYMENT_TYPES = ("Permanent", "Contract")


class ValidationError(ValueError):
    """Raised when an input violates a business rule."""


class InvalidTransitionError(Exception):
    """Raised when a payroll run is moved to a state it cannot reach."""


# ---------------- Input validation ----------------
def validate_basic(basic):
    try:
        basic = float(basic)
    except (TypeError, ValueError):
        raise ValidationError("Basic salary must be a number")
    if basic < MIN_BASIC or basic > MAX_BASIC:
        raise ValidationError(f"Basic salary must be between {MIN_BASIC} and {MAX_BASIC}")
    return basic


def validate_name(name):
    if name is None or len(name) == 0:
        raise ValidationError("Employee name is required")
    if not re.fullmatch(r"[A-Za-z ]{2,50}", name):
        raise ValidationError("Name must be 2-50 letters/spaces")
    return name.strip()


def validate_emp_id(emp_id):
    if not re.fullmatch(r"EMP\d{4}", emp_id or ""):
        raise ValidationError("Employee ID must be 'EMP' followed by 4 digits")
    return emp_id


def validate_employment_type(emp_type):
    if emp_type not in EMPLOYMENT_TYPES:
        raise ValidationError("Employment type must be Permanent or Contract")
    return emp_type


def validate_overtime(hours):
    hours = float(hours)
    if hours < 0 or hours > MAX_OT_HOURS + 1:
        raise ValidationError(f"Overtime hours must be between 0 and {MAX_OT_HOURS}")
    return hours


def validate_lop(days):
    days = float(days)
    if days < 0 or days > MAX_LOP_DAYS:
        raise ValidationError(f"Loss-of-pay days must be between 0 and {MAX_LOP_DAYS}")
    return days


# ---------------- Calculations ----------------
def compute_pf(basic):
    """Employee PF contribution: 12% of basic, basic capped at the PF wage ceiling."""
    return round(basic * PF_RATE, 2)


def compute_professional_tax(gross):
    """Karnataka-style PT: Rs 200 when monthly gross is 25,000 or more."""
    return PT_AMOUNT if gross > PT_THRESHOLD else 0


def compute_bonus(basic, emp_type, years_of_service, rating):
    """Performance bonus per the decision table in 02_Test_Case_Design/03_Decision_Table.md."""
    if emp_type == "Permanent":
        if years_of_service >= 1:
            return round(basic * (0.10 if rating >= 4 else 0.05), 2)
        return 0.0
    # Contract staff
    if rating >= 4:
        return round(basic * 0.05, 2)
    return 0.0


def compute_payslip(basic, overtime_hours=0, lop_days=0, emp_type="Permanent",
                    years_of_service=0, rating=3):
    basic = validate_basic(basic)
    overtime_hours = validate_overtime(overtime_hours)
    lop_days = validate_lop(lop_days)
    validate_employment_type(emp_type)

    hra = round(basic * HRA_RATE, 2)
    da = round(basic * DA_RATE, 2)
    ot_pay = round(overtime_hours * OT_RATE_PER_HOUR, 2)
    lop_deduction = round(basic / DAYS_IN_MONTH * lop_days, 2)
    gross = round(basic + hra + da + ot_pay - lop_deduction, 2)
    bonus = compute_bonus(basic, emp_type, years_of_service, rating)
    pf = compute_pf(basic)
    pt = compute_professional_tax(gross)
    net = round(gross + bonus - pf - pt, 2)
    return {
        "basic": basic, "hra": hra, "da": da, "ot_pay": ot_pay,
        "lop_deduction": lop_deduction, "gross": gross, "bonus": bonus,
        "pf": pf, "professional_tax": pt, "net": net,
    }


# ---------------- Payroll run lifecycle (state machine) ----------------
class PayrollRun:
    """Monthly payroll run: DRAFT -> PROCESSED -> APPROVED -> PAID (or REJECTED -> DRAFT)."""

    TRANSITIONS = {
        ("DRAFT", "process"): "PROCESSED",
        ("PROCESSED", "approve"): "APPROVED",
        ("PROCESSED", "reject"): "REJECTED",
        ("REJECTED", "revise"): "DRAFT",
        ("APPROVED", "pay"): "PAID",
    }

    def __init__(self, month):
        self.month = month
        self.state = "DRAFT"
        self.history = ["DRAFT"]

    def apply(self, event):
        key = (self.state, event)
        if key in self.TRANSITIONS:
            self.state = self.TRANSITIONS[key]
        elif event == "revise" and self.state in ("REJECTED", "PAID"):
            self.state = "DRAFT"
        else:
            raise InvalidTransitionError(f"Cannot '{event}' a payroll run in state {self.state}")
        self.history.append(self.state)
        return self.state
