# Functional Test Cases (end-to-end)

These check complete user flows: login, page protection, and full payslip calculation.

**Example calculation, TC_FN_04** (Permanent, basic 30000, 3 yrs, rating 4, OT 10, LOP 2):

| Item | Formula | Value |
|---|---|---|
| HRA | 40% of 30000 | 12000 |
| DA | 10% of 30000 | 3000 |
| OT pay | 10 × 200 | 2000 |
| LOP | 30000 ÷ 30 × 2 | 2000 |
| **Gross** | 30000 + 12000 + 3000 + 2000 − 2000 | **45000** |
| Bonus | 10% (rule R1) | 3000 |
| PF | 12% of 15000 (ceiling) | 1800 |
| PT | gross ≥ 25000 | 200 |
| **Net** | 45000 + 3000 − 1800 − 200 | **46000** |

| TC ID | Scenario | Test Data | Expected Result |
|---|---|---|---|
| TC_FN_01 | Login with valid credentials | admin / admin@123 | Dashboard opens: 'Welcome, admin' |
| TC_FN_02 | Open dashboard without login | Go to /dashboard | Redirected to /login |
| TC_FN_03 | Payslip for contract employee | Contract, basic 12000, rating 5, OT 0, LOP 0 | Gross 18000, Bonus 600, PF 1440, PT 0, Net 17160 |
| TC_FN_04 | Payslip for permanent employee | Permanent, basic 30000, 3 yrs, rating 4, OT 10, LOP 2 | Gross 45000, Bonus 3000, PF 1800, PT 200, Net 46000 |
