# Test Automation: pytest + Selenium

| File | Tool | What it tests | Tests |
|---|---|---|---|
| [test_payroll.py](test_payroll.py) | **pytest** | Calculation and validation functions in `payroll.py` (BVA, Decision Table, State Transition, EP) | 27 |
| [test_ui_selenium.py](test_ui_selenium.py) | **Selenium WebDriver** | The website in Chrome, like a real user: login, add employee, payslip, payroll run | 8 |
| [conftest.py](conftest.py) | pytest setup | Starts the Flask app automatically, opens Chrome, saves a screenshot of every UI test | |

Every test name starts with its Test Case ID (e.g. `test_TC_BVA_06_...`), so it matches the test case documents.

## How to run

```bash
python -m pip install -r requirements.txt
cd 05_Test_Automation

python -m pytest -v                                # run all 35 tests
python -m pytest test_payroll.py -v                # only pytest (logic) tests
python -m pytest test_ui_selenium.py -v            # only Selenium (browser) tests
python -m pytest -v --html=../06_Test_Reports/test_report.html --self-contained-html   # with HTML report
```

**For the live demo** (the browser moves slowly so you can see each step):

```bash
# PowerShell
$env:SLOW="1"; python -m pytest test_ui_selenium.py -v
```

You don't need to start `app.py` yourself. The tests start it on port 5001.

## Example Selenium test

```python
def test_TC_EP_07_invalid_password_shows_error(driver, login):
    login("admin", "wrong")                       # types into the form and clicks Login
    assert driver.find_element(By.ID, "login-error").text == "Invalid username or password"
```

## Result

**35 tests: 27 passed, 8 failed.** The 8 failures are real bugs in the application, reported in [04_Defect_Reports](../04_Defect_Reports/Defect_Report.md).
