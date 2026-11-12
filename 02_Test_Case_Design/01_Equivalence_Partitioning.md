# Equivalence Partitioning (EP)

**What it is:** Divide inputs into groups (classes) that behave the same way, then test **one value from each group**.

| Input | Valid class | Invalid classes |
|---|---|---|
| Employee ID | EMP + 4 digits (EMP1001) | Wrong format (EMP12) |
| Name | 2-50 letters/spaces | Has digits (Ravi123), only spaces |
| Years of service | Number ≥ 0 | Text (abc) |
| Rating | 1 to 5 | Above 5 (9) |
| Login | Correct username + password | Wrong password |

| TC ID | Scenario | Test Data | Expected Result |
|---|---|---|---|
| TC_EP_01 | Add employee with all valid data | EMP1001, Priya Sharma, Permanent, 30000, 3 yrs, rating 4 | 'Employee EMP1001 added successfully'; shown on dashboard |
| TC_EP_02 | Employee ID in wrong format | ID = EMP12 | Error: ID must be EMP + 4 digits |
| TC_EP_03 | Name containing digits | Name = Ravi123 | Error: Name must be letters/spaces |
| TC_EP_04 | Name with only spaces | Name = "   " | Error: Name is required |
| TC_EP_05 | Text entered in Years of Service | Years = abc | Validation error message on the form |
| TC_EP_06 | Rating outside 1-5 | Rating = 9 | Error: rating must be 1-5; employee not saved |
| TC_EP_07 | Login with wrong password | admin / wrong | 'Invalid username or password' |
