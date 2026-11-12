# Screenshots

## Taken automatically by Selenium (`selenium/` folder)

| Screenshot | Test | Result |
|---|---|---|
| ![](selenium/test_TC_FN_01_valid_login_opens_dashboard.png) | TC_FN_01: valid login opens dashboard | ✅ Pass |
| ![](selenium/test_TC_EP_07_invalid_password_shows_error.png) | TC_EP_07: wrong password shows error | ✅ Pass |
| ![](selenium/test_TC_EP_01_add_valid_employee.png) | TC_EP_01: add valid employee | ✅ Pass |
| ![](selenium/test_TC_FN_03_generate_payslip_contract_employee.png) | TC_FN_03: payslip generated correctly | ✅ Pass |
| ![](selenium/test_TC_EP_05_text_in_years_shows_validation_error.png) | TC_EP_05: "abc" in Years crashes the page | ❌ Fail (DEF-06) |
| ![](selenium/test_TC_EP_06_rating_above_5_rejected.png) | TC_EP_06: rating 9 is saved | ❌ Fail (DEF-06) |
| ![](selenium/test_TC_ST_05_paid_run_cannot_be_revised.png) | TC_ST_05: PAID run revised to DRAFT | ❌ Fail (DEF-04) |

## To add manually

| File name | What to capture |
|---|---|
| `01_pytest_terminal.png` | Terminal after `pytest -v` showing 27 passed, 8 failed |
| `02_html_report.png` | `06_Test_Reports/test_report.html` opened in the browser |
| `03_test_execution_excel.png` | `Test_Execution.xlsx` with Pass/Fail colours |
| `04_github_commits.png` | GitHub commit history page |
