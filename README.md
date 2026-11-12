# Software Testing Portfolio: Employee Payroll Management System

## Student / Team Details

| Name | USN |
|---|---|
| Prisha Kulkarni | 1MS23IS098 |
| Rajeshwari | 1MS23IS099 |

- **Subject:** Software Testing : Other Component
- **Department:** Information Science and Engineering, Ramaiah Institute of Technology, Bangalore
- **Semester:** VII
- **Faculty:** Pushpalata

## Objectives
1. Understand a real-world application and derive testable business rules from it.
2. Prepare a structured **test plan** (IEEE 829 style).
3. Design test cases using **Equivalence Partitioning, Boundary Value Analysis, Decision Tables and State Transition** testing.
4. Execute the tests, record actual results and **identify, document and classify defects**.
5. Automate testing with **pytest** (data-driven unit and functional tests) and **Selenium WebDriver** (UI tests).
6. Maintain all work as a version-controlled portfolio on GitHub.

## Project Description

The **Employee Payroll Management System** is a Flask web application. HR/Admin uses it to add employees, generate monthly payslips (HRA, DA, overtime, loss of pay, bonus, PF, professional tax) and take the monthly payroll through an approval workflow. It is the **application under test**, in [`Application_Under_Test/`](Application_Under_Test).

| Module | Page |
|---|---|
| Login | `/login` |
| Employee Management | `/employees/add`, `/dashboard` |
| Payslip | `/payslip` |
| Payroll Run | `/payroll-run` (DRAFT → PROCESSED → APPROVED → PAID) |

## Repository Structure

| Folder | Contents |
|---|---|
| [01_Test_Plan](01_Test_Plan/Test_Plan.md) | Test plan with business rules R1-R16, scope, approach, entry/exit criteria |
| [02_Test_Case_Design](02_Test_Case_Design/README.md) | 35 test cases: EP, BVA, Decision Table, State Transition, Functional (+ Excel) |
| [03_Test_Execution](03_Test_Execution/Test_Execution_Report.md) | Expected vs actual results, Pass/Fail (+ Excel) |
| [04_Defect_Reports](04_Defect_Reports/Defect_Report.md) | 6 defects with steps, severity, cause and fix (+ Excel) |
| [05_Test_Automation](05_Test_Automation/README.md) | pytest and Selenium test scripts |
| [06_Test_Reports](06_Test_Reports/Test_Summary_Report.md) | Test summary report + pytest HTML report |
| [07_Screenshots](07_Screenshots/README.md) | Selenium screenshots of each UI test |
| [Conclusion.md](Conclusion.md) | Findings and learnings |

## Results

| Test cases | Passed | Failed | Pass % | Defects found |
|---|---|---|---|---|
| 35 | 27 | 8 | 77.1% | 6 (1 Critical, 4 Major, 1 Minor) |

## How to Run

```bash
python -m pip install -r 05_Test_Automation/requirements.txt

# run the application
cd Application_Under_Test
python app.py            # open http://127.0.0.1:5000  (login: admin / admin@123)

# run the tests (in another terminal)
cd 05_Test_Automation
python -m pytest -v
```
