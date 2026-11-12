# Conclusion

We tested the **Employee Payroll Management System**, a Flask web application with 4 modules (Login, Employee Management, Payslip, Payroll Run).

## What we did

1. Wrote a **test plan** with 16 business rules (R1-R16).
2. Designed **35 test cases** using 4 techniques: Equivalence Partitioning (7), Boundary Value Analysis (12), Decision Table (6) and State Transition (6), plus 4 functional tests.
3. Automated all of them: **pytest** for the calculation logic and **Selenium** for the website.
4. Executed the tests: **27 passed, 8 failed (77.1% pass rate)**.
5. Reported **6 defects**: 1 Critical, 4 Major, 1 Minor.

## Key findings

- **BVA was the most useful technique.** It found 3 defects, all exactly at a limit: overtime 61 hours accepted, PF not capped above 15,000, and PT missed at exactly 25,000.
- The most serious bug is **DEF-02**: PF is not capped, so every employee with basic above 15,000 gets a lower salary.
- **State transition testing** showed a PAID payroll can be reopened (DEF-04), which risks paying salaries twice.
- **Selenium** found a crash (DEF-06) that can only be seen through the website.
- The bonus logic (decision table) was fully correct.

## Verdict

The application is **not ready for release** until the Critical and Major defects are fixed and all tests are re-run.

## What we learned

- How to choose a technique: limits call for BVA, combinations call for a decision table, and workflows call for state transition testing.
- How to write clear test cases and defect reports.
- How to automate tests with pytest and Selenium.
- How to maintain a project on GitHub as a team.
