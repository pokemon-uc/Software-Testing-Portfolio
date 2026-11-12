# Test Execution Report

**Date:** 12-11-2026 | **Executed by:** Prisha Kulkarni, Rajeshwari | **Environment:** Windows 11, Python 3.11, pytest 9, Selenium 4, Chrome

| Total | Passed | Failed | Pass % |
|---|---|---|---|
| 35 | 27 | 8 | 77.1% |

## Equivalence Partitioning (4/7 passed)

| TC ID | Scenario | Expected | Actual | Status | Defect | Tool |
|---|---|---|---|---|---|---|
| TC_EP_01 | Add employee with all valid data | 'Employee EMP1001 added successfully'; shown on dashboard | As expected | ✅ Pass | - | Selenium |
| TC_EP_02 | Employee ID in wrong format | Error: ID must be EMP + 4 digits | As expected | ✅ Pass | - | pytest |
| TC_EP_03 | Name containing digits | Error: Name must be letters/spaces | As expected | ✅ Pass | - | pytest |
| TC_EP_04 | Name with only spaces | Error: Name is required | Accepted. No error, and a blank name is stored | ❌ Fail | DEF-05 | pytest |
| TC_EP_05 | Text entered in Years of Service | Validation error message on the form | Page crashed: '500 Internal Server Error' | ❌ Fail | DEF-06 | Selenium |
| TC_EP_06 | Rating outside 1-5 | Error: rating must be 1-5; employee not saved | Employee saved with rating 9, no error | ❌ Fail | DEF-06 | Selenium |
| TC_EP_07 | Login with wrong password | 'Invalid username or password' | As expected | ✅ Pass | - | Selenium |
## Boundary Value Analysis (9/12 passed)

| TC ID | Scenario | Expected | Actual | Status | Defect | Tool |
|---|---|---|---|---|---|---|
| TC_BVA_01 | Basic just below minimum | Rejected | As expected | ✅ Pass | - | pytest |
| TC_BVA_02 | Basic at minimum | Accepted | As expected | ✅ Pass | - | pytest |
| TC_BVA_03 | Basic at maximum | Accepted | As expected | ✅ Pass | - | pytest |
| TC_BVA_04 | Basic just above maximum | Rejected | As expected | ✅ Pass | - | pytest |
| TC_BVA_05 | Overtime at maximum | Accepted; OT pay = 12000 | As expected | ✅ Pass | - | pytest |
| TC_BVA_06 | Overtime just above maximum | Rejected | Accepted. 61 hours allowed | ❌ Fail | DEF-01 | pytest |
| TC_BVA_07 | LOP at maximum | Accepted; deduction = 30000 | As expected | ✅ Pass | - | pytest |
| TC_BVA_08 | LOP just above maximum | Rejected | As expected | ✅ Pass | - | pytest |
| TC_BVA_09 | PF at the 15,000 ceiling | PF = 1800 | As expected | ✅ Pass | - | pytest |
| TC_BVA_10 | PF above the ceiling | PF = 1800 (capped) | PF = 2400 (not capped) | ❌ Fail | DEF-02 | pytest |
| TC_BVA_11 | PT at threshold | PT = 200 | PT = 0 | ❌ Fail | DEF-03 | pytest |
| TC_BVA_12 | PT just below threshold | PT = 0 | As expected | ✅ Pass | - | pytest |
## Decision Table (6/6 passed)

| TC ID | Scenario | Expected | Actual | Status | Defect | Tool |
|---|---|---|---|---|---|---|
| TC_DT_01 | Rule R1: Permanent, years ≥ 1, rating ≥ 4 | Bonus 10% = 2000 | As expected | ✅ Pass | - | pytest |
| TC_DT_02 | Rule R2: Permanent, years ≥ 1, rating < 4 | Bonus 5% = 1000 | As expected | ✅ Pass | - | pytest |
| TC_DT_03 | Rule R3: Permanent, years < 1, rating ≥ 4 | Bonus 0 | As expected | ✅ Pass | - | pytest |
| TC_DT_04 | Rule R4: Permanent, years < 1, rating < 4 | Bonus 0 | As expected | ✅ Pass | - | pytest |
| TC_DT_05 | Rule R5: Contract, rating ≥ 4 | Bonus 5% = 1000 | As expected | ✅ Pass | - | pytest |
| TC_DT_06 | Rule R6: Contract, rating < 4 | Bonus 0 | As expected | ✅ Pass | - | pytest |
## State Transition (5/6 passed)

| TC ID | Scenario | Expected | Actual | Status | Defect | Tool |
|---|---|---|---|---|---|---|
| TC_ST_01 | DRAFT → process | State = PROCESSED | As expected | ✅ Pass | - | pytest |
| TC_ST_02 | Full valid path | State = PAID; history DRAFT→PROCESSED→APPROVED→PAID | As expected | ✅ Pass | - | pytest |
| TC_ST_03 | Reject and revise | REJECTED, then DRAFT | As expected | ✅ Pass | - | pytest |
| TC_ST_04 | Invalid: pay a DRAFT run | Error; state stays DRAFT | As expected | ✅ Pass | - | pytest |
| TC_ST_05 | Invalid: revise a PAID run | Error; state stays PAID | No error. State changed PAID → DRAFT | ❌ Fail | DEF-04 | Selenium |
| TC_ST_06 | Invalid: process a PAID run | Error | As expected | ✅ Pass | - | pytest |
## Functional (3/4 passed)

| TC ID | Scenario | Expected | Actual | Status | Defect | Tool |
|---|---|---|---|---|---|---|
| TC_FN_01 | Login with valid credentials | Dashboard opens: 'Welcome, admin' | As expected | ✅ Pass | - | Selenium |
| TC_FN_02 | Open dashboard without login | Redirected to /login | As expected | ✅ Pass | - | Selenium |
| TC_FN_03 | Payslip for contract employee | Gross 18000, Bonus 600, PF 1440, PT 0, Net 17160 | As expected | ✅ Pass | - | Selenium |
| TC_FN_04 | Payslip for permanent employee | Gross 45000, Bonus 3000, PF 1800, PT 200, Net 46000 | PF = 3600, so Net = 44200 (employee underpaid by 1800) | ❌ Fail | DEF-02 | pytest |

Excel version: [Test_Execution.xlsx](Test_Execution.xlsx) | HTML report from pytest: [../06_Test_Reports/test_report.html](../06_Test_Reports/test_report.html)
