# Boundary Value Analysis (BVA)

**What it is:** Bugs usually happen at the **edges** of a range, so we test values **on** and **just outside** each limit.

| Input | Valid range / limit | Values tested |
|---|---|---|
| Basic salary | 10,000 - 5,00,000 | 9999, 10000, 500000, 500001 |
| Overtime hours | 0 - 60 | 60, 61 |
| LOP days | 0 - 30 | 30, 31 |
| PF ceiling | basic counted up to 15,000 | 15000, 20000 |
| Professional Tax | gross ≥ 25,000 | 24999, 25000 |

| TC ID | Scenario | Test Data | Expected Result |
|---|---|---|---|
| TC_BVA_01 | Basic just below minimum | Basic = 9999 | Rejected |
| TC_BVA_02 | Basic at minimum | Basic = 10000 | Accepted |
| TC_BVA_03 | Basic at maximum | Basic = 500000 | Accepted |
| TC_BVA_04 | Basic just above maximum | Basic = 500001 | Rejected |
| TC_BVA_05 | Overtime at maximum | OT = 60 hrs | Accepted; OT pay = 12000 |
| TC_BVA_06 | Overtime just above maximum | OT = 61 hrs | Rejected |
| TC_BVA_07 | LOP at maximum | Basic 30000, LOP = 30 | Accepted; deduction = 30000 |
| TC_BVA_08 | LOP just above maximum | LOP = 31 | Rejected |
| TC_BVA_09 | PF at the 15,000 ceiling | Basic = 15000 | PF = 1800 |
| TC_BVA_10 | PF above the ceiling | Basic = 20000 | PF = 1800 (capped) |
| TC_BVA_11 | PT at threshold | Gross = 25000 | PT = 200 |
| TC_BVA_12 | PT just below threshold | Gross = 24999 | PT = 0 |
