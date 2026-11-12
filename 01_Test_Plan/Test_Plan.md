# Test Plan: Employee Payroll Management System

## Business Rules
R1: Basic salary must be a number, between 10,000 and 5,00,000
R2: Employee ID must be 'EMP' followed by 4 digits

## Modules

| # | Module | What it does |
|---|---|---|
| M1 | Login | Admin logs in and logs out; pages are protected without login |
| M2 | Employee Management | Admin adds employees with ID, name, type, basic salary, years of service and rating |
| M3 | Payslip | Generates a monthly payslip showing earnings, deductions and net salary |
| M4 | Payroll Run | Takes the month's payroll through Process, Approve/Reject, Revise and Pay |