# Decision Table: Performance Bonus (Rule R14)

**What it is:** When the result depends on a **combination of conditions**, list every combination as a rule and test each rule once.

**Conditions:** C1 = Employment type, C2 = Years of service ≥ 1, C3 = Rating ≥ 4

| | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|
| **C1: Type** | Permanent | Permanent | Permanent | Permanent | Contract | Contract |
| **C2: Years ≥ 1** | Y | Y | N | N | - (any) | - (any) |
| **C3: Rating ≥ 4** | Y | N | Y | N | Y | N |
| **Bonus** | **10%** | **5%** | **0** | **0** | **5%** | **0** |
| Test case | TC_DT_01 | TC_DT_02 | TC_DT_03 | TC_DT_04 | TC_DT_05 | TC_DT_06 |

"-" means the condition does not matter for contract staff, so 8 combinations reduce to 6 rules.

| TC ID | Scenario | Test Data | Expected Result |
|---|---|---|---|
| TC_DT_01 | Rule R1: Permanent, years ≥ 1, rating ≥ 4 | Basic 20000, 3 yrs, rating 4 | Bonus 10% = 2000 |
| TC_DT_02 | Rule R2: Permanent, years ≥ 1, rating < 4 | Basic 20000, 3 yrs, rating 3 | Bonus 5% = 1000 |
| TC_DT_03 | Rule R3: Permanent, years < 1, rating ≥ 4 | Basic 20000, 0 yrs, rating 5 | Bonus 0 |
| TC_DT_04 | Rule R4: Permanent, years < 1, rating < 4 | Basic 20000, 0 yrs, rating 2 | Bonus 0 |
| TC_DT_05 | Rule R5: Contract, rating ≥ 4 | Basic 20000, 2 yrs, rating 5 | Bonus 5% = 1000 |
| TC_DT_06 | Rule R6: Contract, rating < 4 | Basic 20000, 2 yrs, rating 3 | Bonus 0 |
