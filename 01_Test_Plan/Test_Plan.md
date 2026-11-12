# Test Plan: Employee Payroll Management System

| | |
|---|---|
| **Prepared by** | Prisha Kulkarni (1MS23IS098), Rajeshwari (1MS23IS099) |
| **Application** | Employee Payroll Management System (Flask web app), `Application_Under_Test/` |
| **Version** | 1.0 |

## 1. Objective

To check that the payroll system **validates inputs correctly**, **calculates salary correctly** and **allows only valid payroll-run actions**, and to find and report defects before release.

## 2. Modules

| # | Module | What it does |
|---|---|---|
| M1 | Login | Admin logs in and logs out; pages are protected without login |
| M2 | Employee Management | Admin adds employees with ID, name, type, basic salary, years of service and rating |
| M3 | Payslip | Generates a monthly payslip showing earnings, deductions and net salary |
| M4 | Payroll Run | Takes the month's payroll through Process, Approve/Reject, Revise and Pay |

## 3. Business rules (test basis)

| Rule | Description |
|---|---|
| R1 | Basic salary must be a number, between 10,000 and 5,00,000 |
| R2 | Employee ID must be 'EMP' followed by 4 digits (e.g. EMP1001) |
| R3 | HRA = 40% of basic |
| R4 | DA = 10% of basic |
| R5 | Gross = Basic + HRA + DA + Overtime pay − LOP deduction |
| R6 | Net = Gross + Bonus − PF − Professional Tax |
| R7 | Overtime hours allowed 0 to 60; overtime pay = hours × Rs 200 |
| R8 | Loss-of-pay days allowed 0 to 30; LOP deduction = (Basic ÷ 30) × LOP days |
| R9 | PF = 12% of basic, but basic is counted only up to 15,000 (max PF = Rs 1,800) |
| R10 | Professional Tax = Rs 200 if gross ≥ 25,000, otherwise 0 |
| R11 | Name is required: 2-50 letters and spaces |
| R12 | Employment type must be Permanent or Contract |
| R13 | Years of service must be a number ≥ 0; performance rating must be a whole number from 1 to 5 |
| R14 | Bonus: Permanent with ≥ 1 year: 10% of basic if rating ≥ 4, else 5%. Permanent with < 1 year: 0. Contract: 5% if rating ≥ 4, else 0 |
| R15 | Payroll run: DRAFT → PROCESSED → APPROVED → PAID. PROCESSED → REJECTED → (revise) → DRAFT. **PAID is final.** |
| R16 | Login: admin / admin@123. Pages other than Login need a logged-in user |

## 4. Scope

**In scope:** M1-M4, input validation, salary calculations, payroll-run workflow, UI flows.

**Out of scope:** performance/load testing, security testing, database (data is stored in memory), browsers other than Chrome.

## 5. Test approach

| Technique | Where we use it | Why |
|---|---|---|
| Equivalence Partitioning (EP) | Add Employee form, Login | Inputs fall into valid/invalid groups, so one value per group is enough |
| Boundary Value Analysis (BVA) | Basic salary, overtime, LOP, PF ceiling, PT threshold | Payroll has many limits, and bugs usually hide at the edges |
| Decision Table | Bonus (R14) | Bonus depends on a combination of 3 conditions |
| State Transition | Payroll Run (R15) | Allowed actions depend on the current state |

**Automation tools:**
- **pytest**: tests the calculation and validation functions in `payroll.py`
- **Selenium WebDriver**: opens Chrome and tests the website like a real user (login, add employee, payslip, payroll run)

## 6. Entry and exit criteria

| Entry criteria | Exit criteria |
|---|---|
| Business rules R1-R16 are written down | All planned test cases are executed |
| Application runs (`python app.py`) | All failed tests are logged as defects |
| Python, pytest, Selenium and Chrome are installed | Test summary report is prepared |

## 7. Roles

| Member | Responsibility |
|---|---|
| Prisha Kulkarni | Test plan, EP and Decision Table test cases, Selenium UI tests |
| Rajeshwari | BVA and State Transition test cases, pytest tests, defect reports |
| Both | Test execution, summary report, GitHub maintenance |

## 8. Test environment

Windows 11, Python 3.11, Flask, pytest 9, Selenium 4, Google Chrome, VS Code, Git/GitHub.

## 9. Deliverables

Test plan (`01`), test cases (`02`), execution results (`03`), defect reports (`04`), automation scripts (`05`), summary report (`06`), screenshots (`07`), conclusion.

## 10. Risks

| Risk | Mitigation |
|---|---|
| A business rule is unclear | Rules R1-R16 are agreed and written before designing test cases |
| Browser/driver version mismatch for Selenium | Selenium Manager downloads the matching driver automatically |
| Limited time | High-risk areas (salary calculation) are tested first |
