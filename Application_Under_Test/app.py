"""
Employee Payroll Management System - Flask web application (System Under Test).

Run:  python app.py      -> http://127.0.0.1:5000
Login: admin / admin@123
"""
from flask import Flask, request, redirect, url_for, session, render_template_string

from payroll import (ValidationError, InvalidTransitionError, PayrollRun, compute_payslip,
                     validate_name, validate_emp_id, validate_basic, validate_employment_type)

app = Flask(__name__)
app.secret_key = "st-portfolio-demo-key"

USERS = {"admin": "admin@123"}
EMPLOYEES = {}                     # emp_id -> dict
PAYROLL_RUN = PayrollRun("2026-11")

BASE = """
<!doctype html><html><head><title>Payroll MS - {{ title }}</title>
<style>
 body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f4f6fa;color:#222}
 header{background:#1f3a68;color:#fff;padding:14px 28px;display:flex;justify-content:space-between;align-items:center}
 header a{color:#fff;margin-left:18px;text-decoration:none}
 main{max-width:860px;margin:28px auto;background:#fff;padding:26px 32px;border-radius:8px;box-shadow:0 1px 4px #0002}
 label{display:block;margin-top:12px;font-weight:600}
 input,select{padding:7px;width:100%;box-sizing:border-box;border:1px solid #bbb;border-radius:4px}
 button{margin-top:16px;padding:9px 20px;background:#1f3a68;color:#fff;border:0;border-radius:4px;cursor:pointer}
 table{border-collapse:collapse;width:100%;margin-top:14px} td,th{border:1px solid #ddd;padding:7px 10px;text-align:left}
 th{background:#eef2f8} .error{color:#b00020;font-weight:600} .ok{color:#126b2f;font-weight:600}
</style></head><body>
<header><strong>Employee Payroll Management System</strong>
{% if session.get('user') %}<nav><a href="/dashboard">Dashboard</a><a href="/employees/add" id="nav-add">Add Employee</a>
<a href="/payslip" id="nav-payslip">Payslip</a><a href="/payroll-run" id="nav-run">Payroll Run</a>
<a href="/logout" id="logout">Logout</a></nav>{% endif %}</header>
<main>{{ body|safe }}</main></body></html>
"""


def page(title, body, **ctx):
    inner = render_template_string(body, **ctx)
    return render_template_string(BASE, title=title, body=inner)


def login_required(view):
    def wrapper(*a, **kw):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*a, **kw)
    wrapper.__name__ = view.__name__
    return wrapper


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("dashboard" if session.get("user") else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        u, p = request.form.get("username", ""), request.form.get("password", "")
        if USERS.get(u) == p:
            session["user"] = u
            return redirect(url_for("dashboard"))
        error = "Invalid username or password"
    return page("Login", """
<h2>Admin Login</h2>
{% if error %}<p class="error" id="login-error">{{ error }}</p>{% endif %}
<form method="post"><label>Username</label><input name="username" id="username">
<label>Password</label><input name="password" id="password" type="password">
<button id="login-btn" type="submit">Login</button></form>""", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return page("Dashboard", """
<h2 id="welcome">Welcome, {{ user }}</h2>
<p>Payroll month: <b>{{ run.month }}</b> &nbsp; | &nbsp; Run status: <b id="run-state">{{ run.state }}</b></p>
<h3>Employees ({{ emps|length }})</h3>
<table id="emp-table"><tr><th>ID</th><th>Name</th><th>Type</th><th>Basic (Rs)</th><th>Years</th><th>Rating</th></tr>
{% for e in emps.values() %}<tr><td>{{ e.emp_id }}</td><td>{{ e.name }}</td><td>{{ e.emp_type }}</td>
<td>{{ '%.2f' % e.basic }}</td><td>{{ e.years }}</td><td>{{ e.rating }}</td></tr>{% endfor %}</table>""",
                user=session["user"], run=PAYROLL_RUN, emps=EMPLOYEES)


@app.route("/employees/add", methods=["GET", "POST"])
@login_required
def add_employee():
    error = msg = None
    if request.method == "POST":
        f = request.form
        try:
            emp_id = validate_emp_id(f.get("emp_id", ""))
            if emp_id in EMPLOYEES:
                raise ValidationError(f"Employee {emp_id} already exists")
            EMPLOYEES[emp_id] = {
                "emp_id": emp_id, "name": validate_name(f.get("name", "")),
                "emp_type": validate_employment_type(f.get("emp_type", "")),
                "basic": validate_basic(f.get("basic", "")),
                "years": float(f.get("years", 0) or 0), "rating": int(f.get("rating", 3) or 3),
            }
            msg = f"Employee {emp_id} added successfully"
        except ValidationError as e:
            error = str(e)
    return page("Add Employee", """
<h2>Add Employee</h2>
{% if error %}<p class="error" id="form-error">{{ error }}</p>{% endif %}
{% if msg %}<p class="ok" id="form-success">{{ msg }}</p>{% endif %}
<form method="post">
<label>Employee ID</label><input name="emp_id" id="emp_id" placeholder="EMP1001">
<label>Name</label><input name="name" id="name">
<label>Employment Type</label><select name="emp_type" id="emp_type"><option>Permanent</option><option>Contract</option></select>
<label>Basic Salary (Rs)</label><input name="basic" id="basic">
<label>Years of Service</label><input name="years" id="years" value="0">
<label>Performance Rating (1-5)</label><input name="rating" id="rating" value="3">
<button id="save-btn" type="submit">Save Employee</button></form>""", error=error, msg=msg)


@app.route("/payslip", methods=["GET", "POST"])
@login_required
def payslip():
    error = slip = emp = None
    if request.method == "POST":
        emp = EMPLOYEES.get(request.form.get("emp_id", ""))
        try:
            if not emp:
                raise ValidationError("Select a valid employee")
            slip = compute_payslip(emp["basic"], request.form.get("ot_hours", 0) or 0,
                                   request.form.get("lop_days", 0) or 0, emp["emp_type"],
                                   emp["years"], emp["rating"])
        except (ValidationError, ValueError) as e:
            error = str(e)
    return page("Payslip", """
<h2>Generate Payslip</h2>
{% if error %}<p class="error" id="payslip-error">{{ error }}</p>{% endif %}
<form method="post"><label>Employee</label><select name="emp_id" id="emp_select">
{% for e in emps.values() %}<option value="{{ e.emp_id }}">{{ e.emp_id }} - {{ e.name }}</option>{% endfor %}</select>
<label>Overtime Hours (0-60)</label><input name="ot_hours" id="ot_hours" value="{{ request.form.get('ot_hours', 0) }}">
<label>Loss-of-Pay Days (0-30)</label><input name="lop_days" id="lop_days" value="{{ request.form.get('lop_days', 0) }}">
<button id="generate-btn" type="submit">Generate</button></form>
{% if slip %}<h3>Payslip: {{ emp.name }} ({{ emp.emp_id }})</h3><table id="payslip-table">
{% for k,label in rows %}<tr><th>{{ label }}</th><td id="ps-{{ k }}">{{ '%.2f' % slip[k] }}</td></tr>{% endfor %}</table>{% endif %}""",
                error=error, slip=slip, emp=emp, emps=EMPLOYEES,
                rows=[("basic", "Basic"), ("hra", "HRA (40%)"), ("da", "DA (10%)"), ("ot_pay", "Overtime Pay"),
                      ("lop_deduction", "LOP Deduction"), ("gross", "Gross Salary"), ("bonus", "Performance Bonus"),
                      ("pf", "PF (Employee)"), ("professional_tax", "Professional Tax"), ("net", "Net Salary")])


@app.route("/payroll-run", methods=["GET", "POST"])
@login_required
def payroll_run():
    error = None
    if request.method == "POST":
        try:
            PAYROLL_RUN.apply(request.form.get("event", ""))
        except InvalidTransitionError as e:
            error = str(e)
    return page("Payroll Run", """
<h2>Payroll Run - {{ run.month }}</h2>
<p>Current state: <b id="run-state">{{ run.state }}</b></p>
{% if error %}<p class="error" id="run-error">{{ error }}</p>{% endif %}
<form method="post">{% for ev in ['process','approve','reject','revise','pay'] %}
<button name="event" value="{{ ev }}" id="ev-{{ ev }}">{{ ev|capitalize }}</button> {% endfor %}</form>
<p>History: {{ run.history|join(' &rarr; ')|safe }}</p>""", run=PAYROLL_RUN, error=error)


def reset_state():
    """Used by automated tests to start from a clean application state."""
    global PAYROLL_RUN
    EMPLOYEES.clear()
    PAYROLL_RUN = PayrollRun("2026-11")


if __name__ == "__main__":
    app.run(debug=False, port=5000)
