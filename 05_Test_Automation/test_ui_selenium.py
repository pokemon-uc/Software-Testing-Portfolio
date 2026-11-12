"""Selenium WebDriver UI tests for the Flask web application.

The Flask app is started automatically by conftest.py (http://127.0.0.1:5001).
Run:  pytest test_ui_selenium.py -v
      set SLOW=1 first to slow the browser down for a live demo.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from conftest import BASE_URL, pause


def add_employee(driver, emp_id, name, emp_type, basic, years="0", rating="3"):
    driver.get(BASE_URL + "/employees/add")
    driver.find_element(By.ID, "emp_id").send_keys(emp_id)
    driver.find_element(By.ID, "name").send_keys(name)
    Select(driver.find_element(By.ID, "emp_type")).select_by_visible_text(emp_type)
    driver.find_element(By.ID, "basic").send_keys(basic)
    years_box = driver.find_element(By.ID, "years")
    years_box.clear()
    years_box.send_keys(years)
    rating_box = driver.find_element(By.ID, "rating")
    rating_box.clear()
    rating_box.send_keys(rating)
    pause()
    driver.find_element(By.ID, "save-btn").click()
    pause()


# ---------------- Login ----------------

def test_TC_FN_01_valid_login_opens_dashboard(driver, login):
    login("admin", "admin@123")
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))  # wait for the redirect
    assert driver.find_element(By.ID, "welcome").text == "Welcome, admin"


def test_TC_EP_07_invalid_password_shows_error(driver, login):
    login("admin", "wrong")
    assert driver.find_element(By.ID, "login-error").text == "Invalid username or password"


def test_TC_FN_02_dashboard_without_login_redirects(driver):
    driver.get(BASE_URL + "/dashboard")
    assert driver.current_url.endswith("/login")


# ---------------- Add Employee ----------------

def test_TC_EP_01_add_valid_employee(driver, login):
    login()
    add_employee(driver, "EMP1001", "Priya Sharma", "Permanent", "30000", "3", "4")
    assert driver.find_element(By.ID, "form-success").text == "Employee EMP1001 added successfully"
    driver.get(BASE_URL + "/dashboard")
    assert "Priya Sharma" in driver.find_element(By.ID, "emp-table").text


def test_TC_EP_05_text_in_years_shows_validation_error(driver, login):
    login()
    add_employee(driver, "EMP1002", "Ravi Kumar", "Permanent", "30000", years="abc")
    assert "Internal Server Error" not in driver.page_source, "Application crashed (HTTP 500)"
    assert driver.find_elements(By.ID, "form-error"), "No validation error shown"


def test_TC_EP_06_rating_above_5_rejected(driver, login):
    login()
    add_employee(driver, "EMP1003", "Sneha Patil", "Contract", "20000", rating="9")
    assert not driver.find_elements(By.ID, "form-success"), "Employee with rating 9 was saved"
    assert driver.find_elements(By.ID, "form-error"), "No validation error shown"


# ---------------- Payslip ----------------

def test_TC_FN_03_generate_payslip_contract_employee(driver, login):
    login()
    add_employee(driver, "EMP1004", "Anil Rao", "Contract", "12000", "0", "5")
    driver.get(BASE_URL + "/payslip")
    Select(driver.find_element(By.ID, "emp_select")).select_by_value("EMP1004")
    pause()
    driver.find_element(By.ID, "generate-btn").click()
    pause()
    assert driver.find_element(By.ID, "ps-gross").text == "18000.00"
    assert driver.find_element(By.ID, "ps-bonus").text == "600.00"
    assert driver.find_element(By.ID, "ps-pf").text == "1440.00"
    assert driver.find_element(By.ID, "ps-professional_tax").text == "0.00"
    assert driver.find_element(By.ID, "ps-net").text == "17160.00"


# ---------------- Payroll Run (state transition) ----------------

def test_TC_ST_05_paid_run_cannot_be_revised(driver, login):
    login()
    driver.get(BASE_URL + "/payroll-run")
    for event in ("process", "approve", "pay"):
        driver.find_element(By.ID, f"ev-{event}").click()
        pause()
    assert driver.find_element(By.ID, "run-state").text == "PAID"

    driver.find_element(By.ID, "ev-revise").click()
    pause()
    assert driver.find_element(By.ID, "run-state").text == "PAID", "PAID payroll was moved back to DRAFT"
    assert driver.find_elements(By.ID, "run-error"), "No error shown for invalid transition"
