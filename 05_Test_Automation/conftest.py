"""Shared pytest setup.

- Makes the application code (Application_Under_Test) importable.
- Starts the Flask app on http://127.0.0.1:5001 for the Selenium tests.
- Opens Chrome, and saves a screenshot of every UI test into 07_Screenshots/selenium/.
"""
import os
import sys
import threading
import time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "Application_Under_Test"))

SCREENSHOT_DIR = os.path.join(ROOT, "07_Screenshots", "selenium")
BASE_URL = "http://127.0.0.1:5001"
SLOW = os.environ.get("SLOW") == "1"         # SLOW=1 -> pause between steps (for live demo)
HEADLESS = os.environ.get("HEADLESS") == "1"  # HEADLESS=1 -> run without opening a browser window


def pause():
    if SLOW:
        time.sleep(0.8)


@pytest.fixture(scope="session")
def server():
    """Run the Flask app in a background thread for the whole test session."""
    from werkzeug.serving import make_server
    import app as flask_app

    srv = make_server("127.0.0.1", 5001, flask_app.app)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield flask_app
    srv.shutdown()


@pytest.fixture(scope="session")
def browser(server):
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,1200")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


@pytest.fixture
def driver(browser, server, request):
    """Fresh application state + logged-out browser for every UI test."""
    server.reset_state()
    browser.delete_all_cookies()
    yield browser
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    name = request.node.name.split("[")[0]
    browser.save_screenshot(os.path.join(SCREENSHOT_DIR, f"{name}.png"))


@pytest.fixture
def login(driver):
    """Returns a helper that logs in through the UI."""
    from selenium.webdriver.common.by import By

    def _login(username="admin", password="admin@123"):
        driver.get(BASE_URL + "/login")
        driver.find_element(By.ID, "username").send_keys(username)
        pause()
        driver.find_element(By.ID, "password").send_keys(password)
        pause()
        driver.find_element(By.ID, "login-btn").click()
        pause()

    return _login
