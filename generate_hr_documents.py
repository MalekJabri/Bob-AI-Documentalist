#!/usr/bin/env python3
"""
Generate realistic HR documents for employee folders.

Usage:
    python generate_hr_documents.py
        Prompt for your last name, then generate a unique set of HR documents
        namespaced to you. Safe to run in parallel with other lab participants.

    python generate_hr_documents.py --user DUPONT
        Generate documents for lab user "DUPONT" (non-interactive).

    python generate_hr_documents.py --seed-misclassifications
        Generate documents with 5 deliberate errors for Lab 3 training.

    python generate_hr_documents.py --dry-run
        Preview what would be generated without writing any files.

    python generate_hr_documents.py --employee 1
        Generate documents for a single employee only (1-based index).

Multi-user isolation:
    Each user's last name is used as a namespace AND as a seed to generate
    a unique but deterministic set of 5 fictional employees. This means:
      - Files go to HR_DUPONT/ instead of HR/
      - Repository path becomes /BOB_LAB/DUPONT/
      - Employee IDs are DUP001–DUP005 (unique per user)
      - Two users never collide in the repository
      - Same user always gets the same employees (reproducible)
"""

import os
import sys
import random
import hashlib
import argparse
from datetime import datetime, date

# ─────────────────────────────────────────────────────────────────────────────
# NAME & ROLE POOLS — used to generate unique employee datasets per user
# ─────────────────────────────────────────────────────────────────────────────

_FIRST_NAMES = [
    "Alice", "Karim", "Sofia", "Thomas", "Lina", "Emma", "Ravi", "Chloe",
    "Lucas", "Amira", "Hugo", "Fatima", "Noah", "Yasmine", "Léa", "Omar",
    "Camille", "Mehdi", "Inès", "Baptiste", "Nadia", "Julien", "Sara",
    "Antoine", "Layla", "Pierre", "Aisha", "Maxime", "Hana", "Théo",
    "Mia", "Axel", "Zara", "Ethan", "Nina", "Louis", "Dina", "Gabriel",
    "Sana", "Raphaël", "Jade", "Victor", "Leila", "Arthur", "Nour",
]

_LAST_NAMES = [
    "Martin", "El Haddad", "Rossi", "Dupont", "Ben Salem", "Bernard",
    "Fontaine", "Sharma", "Petit", "Benali", "Moreau", "Nguyen", "Simon",
    "Laurent", "Dubois", "Garcia", "Lefebvre", "Roux", "Fournier", "Girard",
    "Bonnet", "Mercier", "Lemaire", "Chevalier", "Robin", "Faure", "Morel",
    "Rousseau", "Blanc", "Guerin", "Muller", "Henry", "Perrin", "Morin",
    "Leroy", "Renard", "Clement", "Gauthier", "Charpentier", "Masson",
]

_DEPARTMENTS = [
    ("IT", "Senior Developer", "CC-IT", ["Paris, France", "Lyon, France"]),
    ("Marketing", "Marketing Manager", "CC-MKT", ["Lyon, France", "Paris, France"]),
    ("Human Resources", "HR Specialist", "CC-HR", ["Paris, France", "Bordeaux, France"]),
    ("Sales", "Sales Representative", "CC-SLS", ["Bordeaux, France", "Marseille, France"]),
    ("Finance", "Financial Analyst", "CC-FIN", ["Paris, France", "Lille, France"]),
]

_MANAGERS = [
    "David Chen", "Sophie Laurent", "Marie Dubois", "Jean-Pierre Moreau",
    "Pierre Fontaine", "Isabelle Renard", "Marc Lefevre", "Nathalie Blanc",
    "Christophe Morin", "Sylvie Garnier", "François Petit", "Anne Leclerc",
]

_HIRE_DATES = [
    "2018-03-12", "2018-11-05", "2019-02-18", "2019-07-22", "2020-01-06",
    "2020-03-15", "2020-09-01", "2021-01-10", "2021-06-14", "2021-11-22",
    "2022-02-28", "2022-08-08", "2023-01-16", "2023-05-02", "2023-10-30",
]

_SALARIES = [3600, 3800, 4000, 4200, 4500, 4800, 5000, 5200, 5500, 5800]


# ─────────────────────────────────────────────────────────────────────────────
# EMPLOYEE DATASET GENERATOR
# Derives a deterministic, unique set of 5 employees from the user's last name.
# ─────────────────────────────────────────────────────────────────────────────

def generate_employee_dataset(lab_user: str) -> list:
    """
    Generate a deterministic set of 5 fictional employees seeded from lab_user.
    The same last name always produces the same employees (reproducible).
    Different last names produce different employees (isolated).
    """
    key = lab_user.upper().strip()
    # Create a stable integer seed from the last name
    seed_bytes = hashlib.sha256(key.encode()).digest()
    seed_int = int.from_bytes(seed_bytes[:8], "big")
    rng = random.Random(seed_int)

    # Derive a 3-letter prefix from the last name (e.g. DUPONT → DUP)
    prefix = key[:3].upper().ljust(3, "X")

    # Shuffle pools independently so picks don't correlate
    first_names = rng.sample(_FIRST_NAMES, len(_FIRST_NAMES))
    last_names = rng.sample(_LAST_NAMES, len(_LAST_NAMES))
    managers = rng.sample(_MANAGERS, len(_MANAGERS))
    hire_dates = rng.sample(_HIRE_DATES, len(_HIRE_DATES))
    salaries = rng.sample(_SALARIES, len(_SALARIES))

    # Assign one department per employee (shuffle departments)
    dept_order = list(range(len(_DEPARTMENTS)))
    rng.shuffle(dept_order)

    employees = []
    for i in range(5):
        fn = first_names[i]
        ln = last_names[i]
        dept_idx = dept_order[i]
        dept, position, cc_prefix, locations = _DEPARTMENTS[dept_idx]
        location = rng.choice(locations)
        salary = salaries[i]
        net_salary = round(salary * 0.75)
        hire_date = hire_dates[i]
        manager = managers[i]
        emp_id = f"{prefix}{i+1:03d}"
        email_fn = fn.lower().replace(" ", "")
        email_ln = ln.lower().replace(" ", "").replace(" ", "")
        cost_center = f"{cc_prefix}-{i+1:03d}"

        employees.append({
            "id": emp_id,
            "name": f"{fn} {ln}",
            "first_name": fn,
            "last_name": ln,
            "email": f"{email_fn}.{email_ln}@company.com",
            "position": position,
            "department": dept,
            "hire_date": hire_date,
            "salary": salary,
            "net_salary": net_salary,
            "manager": manager,
            "location": location,
            "cost_center": cost_center,
            "company": "Acme Corporation",
            "company_code": "ACME-FR",
        })

    return employees


# ─────────────────────────────────────────────────────────────────────────────
# MISCLASSIFICATION SEEDS (dynamic — built from generated employees)
# ─────────────────────────────────────────────────────────────────────────────

def derive_misclassification_seeds(employees: list) -> dict:
    """
    Build the 5 misclassification seeds from the generated employee list.
    The same error patterns are always applied to the same employee slots
    (employee index 0→4), regardless of who the employees are.

    Error patterns (same as original Lab 3 design):
      emp[0] payslip          → bare Document, no metadata
      emp[1] employment_contract → wrong class (Contract), missing Department
      emp[2] performance_review  → wrong EmployeeID (000000)
      emp[3] disciplinary_record → bare Document, no metadata at all
      emp[4] exit_notes          → correct class, missing Department + DocType
    """
    e = employees  # shorthand
    return {
        (e[0]["id"], "payslip"): {
            "error": "Uploaded as base Document class with no EmployeeID",
            "intended_class": "HRDocument",
            "intended_doc_type": "Payslip",
            "seeded_class": "Document",
            "seeded_properties": {},
        },
        (e[1]["id"], "employment_contract"): {
            "error": "Uploaded as Contract class (wrong domain), missing Department",
            "intended_class": "HRDocument",
            "intended_doc_type": "EmploymentContract",
            "seeded_class": "Contract",
            "seeded_properties": {
                "EmployeeID": e[1]["id"],
                "FirstName": e[1]["first_name"],
                "LastName": e[1]["last_name"],
                # Department intentionally omitted
            },
        },
        (e[2]["id"], "performance_review"): {
            "error": f"Uploaded with wrong EmployeeID (000000 instead of {e[2]['id']})",
            "intended_class": "HRDocument",
            "intended_doc_type": "PerformanceReview",
            "seeded_class": "HRDocument",
            "seeded_properties": {
                "EmployeeID": "000000",  # Wrong ID — the error to fix
                "FirstName": e[2]["first_name"],
                "LastName": e[2]["last_name"],
                "DocType": "PerformanceReview",
                "Department": e[2]["department"],
            },
        },
        (e[3]["id"], "disciplinary_record"): {
            "error": "Uploaded as base Document class with no metadata at all",
            "intended_class": "HRDocument",
            "intended_doc_type": "DisciplinaryRecord",
            "seeded_class": "Document",
            "seeded_properties": {},
        },
        (e[4]["id"], "exit_notes"): {
            "error": "Correct class but missing Department and DocType",
            "intended_class": "HRDocument",
            "intended_doc_type": "ExitDocument",
            "seeded_class": "HRDocument",
            "seeded_properties": {
                "EmployeeID": e[4]["id"],
                "FirstName": e[4]["first_name"],
                "LastName": e[4]["last_name"],
                # Department and DocType intentionally omitted
            },
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# LEGACY STATIC EMPLOYEE DATA (kept for backward compatibility / single-user mode)
# Used only when --user is not provided AND the user skips the interactive prompt.
# ─────────────────────────────────────────────────────────────────────────────

EMPLOYEES = [
    {
        "id": "000123",
        "name": "Alice Martin",
        "first_name": "Alice",
        "last_name": "Martin",
        "email": "alice.martin@company.com",
        "position": "Senior Developer",
        "department": "IT",
        "hire_date": "2020-03-15",
        "salary": 5200,
        "net_salary": 3890,
        "manager": "David Chen",
        "location": "Paris, France",
        "cost_center": "CC-IT-001",
        "company": "Acme Corporation",
        "company_code": "ACME-FR",
    },
    {
        "id": "000245",
        "name": "Karim El Haddad",
        "first_name": "Karim",
        "last_name": "El Haddad",
        "email": "karim.elhaddad@company.com",
        "position": "Marketing Manager",
        "department": "Marketing",
        "hire_date": "2019-07-22",
        "salary": 4800,
        "net_salary": 3600,
        "manager": "Sophie Laurent",
        "location": "Lyon, France",
        "cost_center": "CC-MKT-002",
        "company": "Acme Corporation",
        "company_code": "ACME-FR",
    },
    {
        "id": "000367",
        "name": "Sofia Rossi",
        "first_name": "Sofia",
        "last_name": "Rossi",
        "email": "sofia.rossi@company.com",
        "position": "HR Specialist",
        "department": "Human Resources",
        "hire_date": "2021-01-10",
        "salary": 4200,
        "net_salary": 3150,
        "manager": "Marie Dubois",
        "location": "Paris, France",
        "cost_center": "CC-HR-003",
        "company": "Acme Corporation",
        "company_code": "ACME-FR",
    },
    {
        "id": "000489",
        "name": "Thomas Dupont",
        "first_name": "Thomas",
        "last_name": "Dupont",
        "email": "thomas.dupont@company.com",
        "position": "Sales Representative",
        "department": "Sales",
        "hire_date": "2018-11-05",
        "salary": 3800,
        "net_salary": 2850,
        "manager": "Jean-Pierre Moreau",
        "location": "Bordeaux, France",
        "cost_center": "CC-SLS-004",
        "company": "Acme Corporation",
        "company_code": "ACME-FR",
    },
    {
        "id": "000512",
        "name": "Lina Ben Salem",
        "first_name": "Lina",
        "last_name": "Ben Salem",
        "email": "lina.bensalem@company.com",
        "position": "Financial Analyst",
        "department": "Finance",
        "hire_date": "2022-02-28",
        "salary": 4500,
        "net_salary": 3375,
        "manager": "Pierre Fontaine",
        "location": "Paris, France",
        "cost_center": "CC-FIN-005",
        "company": "Acme Corporation",
        "company_code": "ACME-FR",
    },
]



# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT GENERATORS
# Each function returns the text content of a specific document type.
# ─────────────────────────────────────────────────────────────────────────────

def generate_job_application(emp):
    return f"""JOB APPLICATION
{"=" * 60}

APPLICANT INFORMATION
---------------------
Full Name:          {emp['name']}
Email Address:      {emp['email']}
Position Applied:   {emp['position']}
Department:         {emp['department']}
Application Date:   {emp['hire_date']}
Location:           {emp['location']}

COVER LETTER
------------
Dear Hiring Manager,

I am writing to express my strong interest in the {emp['position']} position
within the {emp['department']} department at {emp['company']}.

With a proven track record in my field and a passion for delivering results,
I am confident that my skills and experience align well with the requirements
of this role. I am particularly drawn to {emp['company']}'s commitment to
innovation and excellence.

Throughout my career, I have developed strong expertise in my domain,
consistently exceeding targets and contributing to team success. I am a
collaborative team player who thrives in dynamic environments and is always
eager to take on new challenges.

I would welcome the opportunity to discuss how my background and skills
could contribute to your team. Thank you for considering my application.

Best regards,
{emp['name']}
{emp['email']}

DECLARATION
-----------
I hereby declare that all information provided in this application is
accurate and complete to the best of my knowledge.

Signature: {emp['name']}
Date:       {emp['hire_date']}
"""


def generate_interview_notes(emp):
    return f"""INTERVIEW ASSESSMENT NOTES
{"=" * 60}
CONFIDENTIAL — HR USE ONLY

CANDIDATE INFORMATION
---------------------
Candidate Name:     {emp['name']}
Position:           {emp['position']}
Department:         {emp['department']}
Interview Date:     {emp['hire_date']}
Interviewer(s):     {emp['manager']}, HR Representative
Location:           {emp['location']}

ASSESSMENT SCORES (1-5 scale)
------------------------------
Technical Skills:           5 / 5  — Excellent
Communication Skills:       4 / 5  — Very Good
Problem Solving:            5 / 5  — Excellent
Cultural Fit:               5 / 5  — Strong
Leadership Potential:       4 / 5  — Very Good
Overall Score:              4.6 / 5

INTERVIEW NOTES
---------------
Round 1 — Technical Interview:
  The candidate demonstrated exceptional technical knowledge relevant to the
  {emp['position']} role. Answered all technical questions confidently and
  provided concrete examples from previous experience. Showed strong
  analytical thinking and attention to detail.

Round 2 — Behavioural Interview:
  Excellent communication skills. Provided structured, thoughtful responses
  using the STAR method. Demonstrated strong alignment with company values
  including integrity, collaboration, and continuous improvement.

Round 3 — Manager Interview with {emp['manager']}:
  Very positive interaction. Candidate showed genuine enthusiasm for the role
  and the {emp['department']} team. Asked insightful questions about team
  dynamics and growth opportunities.

STRENGTHS IDENTIFIED
--------------------
  - Strong domain expertise
  - Excellent communication and presentation skills
  - Proactive and self-motivated
  - Team-oriented mindset
  - Quick learner with adaptability

AREAS FOR DEVELOPMENT
---------------------
  - Could benefit from broader cross-functional exposure
  - Opportunity to develop leadership skills further

HIRING RECOMMENDATION
---------------------
Decision:   HIRE — STRONGLY RECOMMENDED
Start Date: {emp['hire_date']}
Salary Offer: €{emp['salary']:,}/month gross

Approved by: {emp['manager']}
Date: {emp['hire_date']}
"""


def generate_employment_contract(emp):
    return f"""EMPLOYMENT CONTRACT
{"=" * 60}

This Employment Agreement ("Agreement") is entered into on {emp['hire_date']}
between:

EMPLOYER:
  Company Name:   {emp['company']}
  Company Code:   {emp['company_code']}
  Registered at:  Paris Commercial Register
  Represented by: Human Resources Department

EMPLOYEE:
  Full Name:      {emp['name']}
  Employee ID:    {emp['id']}
  Email:          {emp['email']}
  Location:       {emp['location']}

ARTICLE 1 — POSITION AND DUTIES
--------------------------------
The Employee is hired as {emp['position']} in the {emp['department']} department,
reporting to {emp['manager']}.

The Employee's duties include, but are not limited to:
  - Performing all tasks associated with the {emp['position']} role
  - Collaborating with team members and stakeholders
  - Adhering to company policies and procedures
  - Contributing to departmental and company objectives

ARTICLE 2 — START DATE AND DURATION
-------------------------------------
Start Date:         {emp['hire_date']}
Contract Type:      Permanent (CDI — Contrat à Durée Indéterminée)
Probation Period:   3 months from start date

ARTICLE 3 — WORKING HOURS
--------------------------
Standard Hours:     35 hours per week (French legal standard)
Working Days:       Monday to Friday
Location:           {emp['location']}
Remote Work:        Up to 2 days per week subject to manager approval

ARTICLE 4 — REMUNERATION
-------------------------
Gross Monthly Salary:   €{emp['salary']:,}
Net Monthly Salary:     €{emp['net_salary']:,} (approximate)
Payment Date:           Last working day of each month
Cost Center:            {emp['cost_center']}

ARTICLE 5 — BENEFITS
---------------------
  - 25 days paid annual leave
  - Health insurance (mutuelle) — 50% employer contribution
  - Meal vouchers — €9.50/day
  - Transport allowance — 50% of public transport pass
  - Pension scheme — employer contribution per legal requirements

ARTICLE 6 — CONFIDENTIALITY
----------------------------
The Employee agrees to maintain strict confidentiality regarding all
proprietary information, trade secrets, and business data encountered
during the course of employment.

ARTICLE 7 — TERMINATION
------------------------
Either party may terminate this agreement with notice:
  - During probation: 1 week notice
  - After probation: 1 month notice (employee) / 2 months (employer)

SIGNATURES
----------
Employee:   {emp['name']}          Date: {emp['hire_date']}
Employer:   {emp['manager']}       Date: {emp['hire_date']}
HR:         HR Department          Date: {emp['hire_date']}
"""


def generate_id_documents(emp):
    return f"""IDENTITY DOCUMENT RECORD
{"=" * 60}
CONFIDENTIAL — RESTRICTED ACCESS

EMPLOYEE INFORMATION
--------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Date Recorded:      {emp['hire_date']}
Recorded by:        HR Department

IDENTITY DOCUMENTS ON FILE
---------------------------
Document Type:      National Identity Card
Document Number:    [REDACTED FOR PRIVACY]
Issue Date:         [REDACTED FOR PRIVACY]
Expiry Date:        [REDACTED FOR PRIVACY]
Issuing Authority:  French Government
Status:             ✓ VERIFIED

Document Type:      Social Security Number (NIR)
Number:             [REDACTED FOR PRIVACY]
Status:             ✓ VERIFIED

Document Type:      Work Authorization
Status:             ✓ EU Citizen — No restriction

RIGHT TO WORK VERIFICATION
---------------------------
Verification Date:  {emp['hire_date']}
Verified by:        HR Department
Result:             APPROVED — Full right to work in France

DATA PROTECTION NOTICE
-----------------------
Identity documents are stored in compliance with GDPR Article 9.
Access is restricted to authorized HR personnel only.
Retention period: Duration of employment + 5 years.

Authorized by: HR Department
Date: {emp['hire_date']}
"""


def generate_personal_info(emp):
    return f"""PERSONAL INFORMATION FORM
{"=" * 60}

EMPLOYEE DETAILS
----------------
Full Name:          {emp['name']}
Employee ID:        {emp['id']}
Email (Work):       {emp['email']}
Department:         {emp['department']}
Position:           {emp['position']}
Start Date:         {emp['hire_date']}
Work Location:      {emp['location']}
Cost Center:        {emp['cost_center']}
Reporting Manager:  {emp['manager']}

EMERGENCY CONTACT
-----------------
[Provided separately — stored in HR system]

BANK DETAILS FOR PAYROLL
------------------------
Bank:               [Provided separately — stored in secure HR system]
IBAN:               [REDACTED]
BIC:                [REDACTED]

PERSONAL PREFERENCES
--------------------
Preferred Language:     French
Communication Method:   Email
Newsletter:             Yes
Training Notifications: Yes

DATA CONSENT
------------
I consent to {emp['company']} processing my personal data for employment
purposes in accordance with GDPR and the company's Privacy Policy.

Employee Signature: {emp['name']}
Date: {emp['hire_date']}
"""


def generate_payslip(emp, month="January", year="2024"):
    gross = emp['salary']
    social_contributions = round(gross * 0.22, 2)
    income_tax = round(gross * 0.08, 2)
    net = gross - social_contributions - income_tax

    return f"""PAYSLIP
{"=" * 60}

EMPLOYER INFORMATION
--------------------
Company:            {emp['company']}
Company Code:       {emp['company_code']}
SIRET:              123 456 789 00012
Address:            1 Rue de la Paix, 75001 Paris, France

EMPLOYEE INFORMATION
--------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Position:           {emp['position']}
Cost Center:        {emp['cost_center']}

PAY PERIOD
----------
Month:              {month} {year}
Working Days:       22 days
Hours Worked:       154 hours

EARNINGS
--------
Basic Salary:                       €{gross:,.2f}
Overtime (0h):                      €0.00
Bonus:                              €0.00
                                    ─────────────
GROSS SALARY:                       €{gross:,.2f}

DEDUCTIONS
----------
Social Security Contributions:      -€{social_contributions:,.2f}
  (Health, Pension, Unemployment)
Income Tax (Withholding):           -€{income_tax:,.2f}
                                    ─────────────
TOTAL DEDUCTIONS:                   -€{social_contributions + income_tax:,.2f}

NET PAY
-------
NET SALARY:                         €{net:,.2f}

PAYMENT DATE:       Last working day of {month} {year}
PAYMENT METHOD:     Bank Transfer (IBAN on file)

YEAR-TO-DATE SUMMARY
--------------------
YTD Gross:          €{gross:,.2f}
YTD Net:            €{net:,.2f}
YTD Tax Paid:       €{income_tax:,.2f}

This payslip is generated automatically. Keep for your records.
Employer: {emp['company']} | Employee: {emp['name']} ({emp['id']})
"""


def generate_salary_info(emp):
    return f"""SALARY INFORMATION RECORD
{"=" * 60}
CONFIDENTIAL — HR AND FINANCE USE ONLY

EMPLOYEE INFORMATION
--------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Position:           {emp['position']}
Cost Center:        {emp['cost_center']}
Start Date:         {emp['hire_date']}

CURRENT COMPENSATION
--------------------
Gross Monthly Salary:       €{emp['salary']:,}
Net Monthly Salary:         €{emp['net_salary']:,} (approximate)
Annual Gross Salary:        €{emp['salary'] * 12:,}
Salary Grade:               Grade {3 + (emp['salary'] // 1000)}
Pay Band:                   Band B

SALARY HISTORY
--------------
Date            Event                   Amount
{emp['hire_date']}    Initial Salary          €{emp['salary']:,}/month
(No subsequent changes recorded)

BENEFITS SUMMARY
----------------
Meal Vouchers:          €9.50/day × 22 days = €209/month
Transport Allowance:    50% of Navigo pass (~€40/month)
Health Insurance:       Employer pays 50% of premium
Pension:                Employer contribution per legal requirements

NEXT REVIEW DATE
----------------
Annual salary review scheduled for: January of each year
Last review: N/A (first year)

Prepared by: HR Department
Date: {emp['hire_date']}
"""


def generate_performance_review(emp, year="2024"):
    return f"""ANNUAL PERFORMANCE REVIEW
{"=" * 60}

REVIEW INFORMATION
------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Position:           {emp['position']}
Review Period:      January {year} — December {year}
Review Date:        December 15, {year}
Reviewer:           {emp['manager']}

PERFORMANCE RATINGS (1-5 scale)
--------------------------------
1. Quality of Work:                 4 / 5  — Exceeds Expectations
2. Productivity & Efficiency:       4 / 5  — Exceeds Expectations
3. Communication & Collaboration:   5 / 5  — Outstanding
4. Initiative & Innovation:         4 / 5  — Exceeds Expectations
5. Adherence to Values:             5 / 5  — Outstanding
6. Goal Achievement:                4 / 5  — Exceeds Expectations

OVERALL RATING:                     4.3 / 5 — EXCEEDS EXPECTATIONS

GOALS REVIEW — {year}
-----------------------
Goal 1: [Department-specific goal]
  Status: ✓ ACHIEVED
  Comments: Delivered ahead of schedule with high quality.

Goal 2: [Cross-functional collaboration goal]
  Status: ✓ ACHIEVED
  Comments: Demonstrated excellent teamwork and communication.

Goal 3: [Professional development goal]
  Status: ✓ ACHIEVED
  Comments: Completed all required training and certifications.

STRENGTHS
---------
  - Consistently delivers high-quality work
  - Strong communication and interpersonal skills
  - Proactive in identifying and solving problems
  - Positive attitude and team player
  - Reliable and meets all deadlines

AREAS FOR DEVELOPMENT
---------------------
  - Continue developing leadership and mentoring skills
  - Expand cross-departmental network
  - Pursue advanced certifications in area of expertise

GOALS FOR {int(year) + 1}
-----------------------
  1. Lead at least one cross-functional project
  2. Complete advanced professional certification
  3. Mentor a junior team member
  4. Contribute to departmental strategy planning

COMPENSATION RECOMMENDATION
----------------------------
Salary Increase Recommended:    3.5%
New Salary (if approved):       €{int(emp['salary'] * 1.035):,}/month
Effective Date:                 January 1, {int(year) + 1}

EMPLOYEE COMMENTS
-----------------
"I am proud of my achievements this year and look forward to taking on
greater responsibilities in {int(year) + 1}."
— {emp['name']}

SIGNATURES
----------
Employee:   {emp['name']}          Date: December 15, {year}
Manager:    {emp['manager']}       Date: December 15, {year}
HR:         HR Department          Date: December 20, {year}
"""


def generate_training_record(emp):
    return f"""TRAINING AND DEVELOPMENT RECORD
{"=" * 60}

EMPLOYEE INFORMATION
--------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Position:           {emp['position']}
Record Updated:     {emp['hire_date']}

MANDATORY TRAINING — COMPLETED
--------------------------------
Training                            Date            Status    Score
─────────────────────────────────── ─────────────── ───────── ──────
GDPR & Data Protection              {emp['hire_date']}   ✓ PASSED  92%
Health & Safety Induction           {emp['hire_date']}   ✓ PASSED  88%
Code of Conduct & Ethics            {emp['hire_date']}   ✓ PASSED  95%
Information Security Awareness      {emp['hire_date']}   ✓ PASSED  90%
Anti-Bribery & Corruption           {emp['hire_date']}   ✓ PASSED  87%
Fire Safety & Emergency Procedures  {emp['hire_date']}   ✓ PASSED  100%

PROFESSIONAL DEVELOPMENT — COMPLETED
--------------------------------------
Training                            Provider        Date            Hours
─────────────────────────────────── ─────────────── ─────────────── ──────
Advanced {emp['position'][:20]:<20}  External        {emp['hire_date']}   16h
Leadership Fundamentals             Internal        {emp['hire_date']}   8h
Project Management Essentials       Online (Coursera) {emp['hire_date']} 24h

CERTIFICATIONS
--------------
Certification                       Issuer          Date        Expiry
─────────────────────────────────── ─────────────── ─────────── ──────────
Professional Certification          Industry Body   {emp['hire_date']}  3 years

TRAINING HOURS SUMMARY
----------------------
Mandatory Training:         12 hours
Professional Development:   48 hours
Total Training Hours:       60 hours
Annual Target:              40 hours
Status:                     ✓ TARGET EXCEEDED

UPCOMING TRAINING
-----------------
Training                            Scheduled Date  Status
─────────────────────────────────── ─────────────── ──────────
Annual Compliance Refresh           Q1 next year    Scheduled
Advanced Leadership Program         Q2 next year    Nominated

Approved by: {emp['manager']}
HR Verified: HR Department
"""


def generate_disciplinary_record(emp):
    return f"""DISCIPLINARY RECORD
{"=" * 60}
CONFIDENTIAL — STRICTLY RESTRICTED ACCESS

EMPLOYEE INFORMATION
--------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Position:           {emp['position']}

DISCIPLINARY HISTORY
--------------------
Record Date:        {emp['hire_date']}
Recorded by:        HR Department

Status:             NO ACTIVE DISCIPLINARY PROCEEDINGS

This record confirms that as of {emp['hire_date']}, the above-named employee
has no active disciplinary proceedings, warnings, or sanctions on file.

CONDUCT RECORD
--------------
Verbal Warnings:        0
Written Warnings:       0
Final Warnings:         0
Suspensions:            0
Dismissal Proceedings:  0

NOTES
-----
Employee has maintained a clean disciplinary record since joining the company
on {emp['hire_date']}. No incidents have been reported or investigated.

This document is maintained for compliance purposes and is reviewed annually.

CONFIDENTIALITY NOTICE
----------------------
This record is strictly confidential and may only be accessed by:
  - The employee themselves
  - Their direct line manager
  - HR Department
  - Senior management (in case of escalation)

Access is logged and audited.

Prepared by: HR Department
Date: {emp['hire_date']}
Next Review: Annual
"""


def generate_exit_notes(emp):
    return f"""EXIT INTERVIEW AND OFFBOARDING NOTES
{"=" * 60}
CONFIDENTIAL — HR USE ONLY

EMPLOYEE INFORMATION
--------------------
Employee Name:      {emp['name']}
Employee ID:        {emp['id']}
Department:         {emp['department']}
Position:           {emp['position']}
Start Date:         {emp['hire_date']}
Exit Date:          [Not yet determined — record created at onboarding]

OFFBOARDING STATUS
------------------
Status:             ACTIVE EMPLOYEE — No exit in progress

This document is created at onboarding as a template for future use.
It will be completed upon the employee's departure from the company.

STANDARD OFFBOARDING CHECKLIST (Template)
------------------------------------------
  [ ] Exit interview conducted
  [ ] Knowledge transfer completed
  [ ] Equipment returned (laptop, badge, phone)
  [ ] System access revoked
  [ ] Email forwarding configured
  [ ] Final payslip processed
  [ ] Reference letter issued (if requested)
  [ ] Non-disclosure agreement reminder signed
  [ ] LinkedIn recommendation (optional)

EXIT INTERVIEW QUESTIONS (Template)
-------------------------------------
  1. What is your primary reason for leaving?
  2. What did you enjoy most about working here?
  3. What could the company improve?
  4. Would you recommend {emp['company']} as an employer?
  5. Would you consider returning in the future?

KNOWLEDGE TRANSFER PLAN (To be completed)
------------------------------------------
  - Key responsibilities to be handed over: [TBD]
  - Handover recipient: [TBD]
  - Handover completion date: [TBD]
  - Documentation to be updated: [TBD]

Prepared by: HR Department
Date: {emp['hire_date']}
"""


# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT CATALOG
# Maps (employee_id, doc_key) → (filename, generator_function, doc_type, folder)
# ─────────────────────────────────────────────────────────────────────────────

def build_document_catalog(emp):
    """Build the full list of documents for one employee."""
    eid = emp["id"]
    return [
        {
            "key": "job_application",
            "filename": f"{eid}_Job_Application.txt",
            "folder": "01_Recruitment",
            "doc_type": "JobApplication",
            "content_fn": lambda e=emp: generate_job_application(e),
        },
        {
            "key": "interview_notes",
            "filename": f"{eid}_Interview_Notes.txt",
            "folder": "01_Recruitment",
            "doc_type": "InterviewNotes",
            "content_fn": lambda e=emp: generate_interview_notes(e),
        },
        {
            "key": "employment_contract",
            "filename": f"{eid}_Employment_Contract.txt",
            "folder": "02_Employment_Contract",
            "doc_type": "EmploymentContract",
            "content_fn": lambda e=emp: generate_employment_contract(e),
        },
        {
            "key": "id_documents",
            "filename": f"{eid}_ID_Documents.txt",
            "folder": "03_Personal_Administration",
            "doc_type": "IDDocument",
            "content_fn": lambda e=emp: generate_id_documents(e),
        },
        {
            "key": "personal_info",
            "filename": f"{eid}_Personal_Info.txt",
            "folder": "03_Personal_Administration",
            "doc_type": "PersonalInfo",
            "content_fn": lambda e=emp: generate_personal_info(e),
        },
        {
            "key": "payslip",
            "filename": f"{eid}_Payslip_2024_01.txt",
            "folder": "04_Payroll",
            "doc_type": "Payslip",
            "content_fn": lambda e=emp: generate_payslip(e),
        },
        {
            "key": "salary_info",
            "filename": f"{eid}_Salary_Info.txt",
            "folder": "04_Payroll",
            "doc_type": "SalaryInfo",
            "content_fn": lambda e=emp: generate_salary_info(e),
        },
        {
            "key": "performance_review",
            "filename": f"{eid}_Performance_Review_2024.txt",
            "folder": "05_Performance",
            "doc_type": "PerformanceReview",
            "content_fn": lambda e=emp: generate_performance_review(e),
        },
        {
            "key": "training_record",
            "filename": f"{eid}_Training_Record.txt",
            "folder": "06_Training",
            "doc_type": "TrainingRecord",
            "content_fn": lambda e=emp: generate_training_record(e),
        },
        {
            "key": "disciplinary_record",
            "filename": f"{eid}_Disciplinary_Record.txt",
            "folder": "07_Disciplinary",
            "doc_type": "DisciplinaryRecord",
            "content_fn": lambda e=emp: generate_disciplinary_record(e),
        },
        {
            "key": "exit_notes",
            "filename": f"{eid}_Exit_Notes.txt",
            "folder": "08_Exit",
            "doc_type": "ExitDocument",
            "content_fn": lambda e=emp: generate_exit_notes(e),
        },
    ]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN GENERATION LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def get_seed_info(emp_id, doc_key, seed_misclassifications, misclassification_seeds):
    """Return misclassification seed info if applicable, else None."""
    if not seed_misclassifications:
        return None
    return misclassification_seeds.get((emp_id, doc_key))


def generate_metadata_comment(emp, doc_type, seed_info):
    """
    Generate a metadata comment block appended to each file.
    This helps Bob understand the intended metadata when uploading.
    If seed_info is provided, the comment reflects the seeded (wrong) metadata.
    """
    if seed_info:
        props = seed_info["seeded_properties"]
        lines = [
            "",
            "─" * 60,
            "DOCUMENT METADATA (for repository upload)",
            "─" * 60,
            f"Intended Class:    {seed_info['intended_class']}",
            f"Seeded Class:      {seed_info['seeded_class']}  ← LAB 3 ERROR",
            f"Error Description: {seed_info['error']}",
            "",
            "Properties to set (as seeded — contains errors):",
        ]
        if props:
            for k, v in props.items():
                lines.append(f"  {k}: {v}")
        else:
            lines.append("  (no properties set — bare upload)")
        lines.append("")
        lines.append("NOTE: This document contains a deliberate error for Lab 3.")
        lines.append("Bob should detect and fix this during the classification audit.")
    else:
        lines = [
            "",
            "─" * 60,
            "DOCUMENT METADATA (for repository upload)",
            "─" * 60,
            f"Class:             HRDocument",
            f"EmployeeID:        {emp['id']}",
            f"FirstName:         {emp['first_name']}",
            f"LastName:          {emp['last_name']}",
            f"DocType:           {doc_type}",
            f"Department:        {emp['department']}",
            f"JobRole:           {emp['position']}",
            f"Company:           {emp['company']}",
            f"CompanyCode:       {emp['company_code']}",
            f"CostCenter:        {emp['cost_center']}",
            f"Location:          {emp['location']}",
            f"StartDate:         {emp['hire_date']}",
        ]
    return "\n".join(lines)


def generate_all_documents(
    employees,
    seed_misclassifications=False,
    dry_run=False,
    filter_employee=None,
    lab_user=None,
):
    """Generate all HR documents for all employees.

    Args:
        employees:               List of employee dicts to generate documents for.
        seed_misclassifications: If True, inject 5 deliberate errors for Lab 3.
        dry_run:                 If True, print what would be done without writing files.
        filter_employee:         If set, only generate for this employee ID.
        lab_user:                Uppercase last name used as namespace (e.g. "DUPONT").
                                 If provided, files go to HR_DUPONT/ and seeds are
                                 derived dynamically from the employee list.
                                 If None, falls back to legacy HR/ + static seeds.
    """
    # Determine base directory and misclassification seeds
    if lab_user:
        base_dir = f"HR_{lab_user.upper()}"
        misclassification_seeds = derive_misclassification_seeds(employees)
    else:
        base_dir = "HR"
        misclassification_seeds = derive_misclassification_seeds(employees)

    total_files = 0
    total_seeded = 0

    mode_label = "DRY RUN — " if dry_run else ""
    user_label = f" [{lab_user.upper()}]" if lab_user else ""
    print(f"\n{mode_label}Generating HR Documents{user_label}")
    print("=" * 60)
    if lab_user:
        print(f"📂 Output directory : {base_dir}/")
        print(f"🗂️  Repository path  : /BOB_LAB/{lab_user.upper()}/")
    if seed_misclassifications:
        print("⚠️  Misclassification seeds ENABLED (Lab 3 mode)")
    print()

    for emp in employees:
        if filter_employee and emp["id"] != filter_employee:
            continue

        emp_folder = os.path.join(base_dir, f"{emp['id']}_{emp['name']}")
        print(f"📁 {emp['name']} ({emp['id']}) — {emp['department']}")

        docs = build_document_catalog(emp)

        for doc in docs:
            folder_path = os.path.join(emp_folder, doc["folder"])
            file_path = os.path.join(folder_path, doc["filename"])

            seed_info = get_seed_info(emp["id"], doc["key"], seed_misclassifications, misclassification_seeds)
            content = doc["content_fn"]()
            metadata_comment = generate_metadata_comment(emp, doc["doc_type"], seed_info)
            full_content = content + metadata_comment

            if seed_info:
                status = f"⚠️  SEEDED ERROR: {seed_info['error'][:50]}..."
                total_seeded += 1
            else:
                status = "✅"

            print(f"   {status}")
            print(f"      File:    {doc['filename']}")
            print(f"      Folder:  {doc['folder']}")
            print(f"      DocType: {doc['doc_type']}")

            if not dry_run:
                os.makedirs(folder_path, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(full_content)

            total_files += 1

        print()

    print("=" * 60)
    if dry_run:
        print(f"DRY RUN complete. Would generate {total_files} files.")
    else:
        print(f"✅ Generation complete. {total_files} files written to {base_dir}/")
    if seed_misclassifications:
        print(f"⚠️  {total_seeded} files contain deliberate errors for Lab 3.")
    print()

    return total_files, total_seeded


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def prompt_for_lab_user() -> str:
    """Interactively ask the participant for their last name."""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        Welcome to Lab 2 — HR Document Generation            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("  To avoid conflicts with other lab participants, your documents")
    print("  will be stored in a personal namespace based on your last name.")
    print()
    while True:
        raw = input("  👤 Please enter your last name: ").strip()
        if not raw:
            print("  ⚠️  Last name cannot be empty. Please try again.")
            continue
        # Normalise: uppercase, letters only (allow spaces/hyphens for compound names)
        normalised = raw.upper()
        confirm = input(f"  ✅ Use '{normalised}' as your lab namespace? [Y/n]: ").strip().lower()
        if confirm in ("", "y", "yes"):
            return normalised
        print("  ↩️  Let's try again.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic HR documents for IBM Content Services labs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_hr_documents.py
      Prompt for your last name, then generate your personal employee dataset.

  python generate_hr_documents.py --user DUPONT
      Non-interactive: use DUPONT as the lab namespace.

  python generate_hr_documents.py --user DUPONT --seed-misclassifications
      Generate documents with 5 deliberate errors for Lab 3 training.

  python generate_hr_documents.py --user DUPONT --dry-run
      Preview what would be generated without writing files.

  python generate_hr_documents.py --user DUPONT --employee 1
      Generate documents for the first employee in DUPONT's dataset only.

  python generate_hr_documents.py --user DUPONT --seed-misclassifications --dry-run
      Preview the seeded errors without writing files.
        """
    )
    parser.add_argument(
        "--user",
        type=str,
        metavar="LASTNAME",
        help=(
            "Your last name, used as a lab namespace and employee-dataset seed. "
            "If omitted, you will be prompted interactively."
        ),
    )
    parser.add_argument(
        "--seed-misclassifications",
        action="store_true",
        help="Seed 5 documents with deliberate classification errors for Lab 3."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be generated without writing any files."
    )
    parser.add_argument(
        "--employee",
        type=int,
        metavar="INDEX",
        help="Generate documents for a single employee only (1-based index, e.g. 1)."
    )

    args = parser.parse_args()

    # ── Resolve lab user ──────────────────────────────────────────────────────
    if args.user:
        lab_user = args.user.upper().strip()
    else:
        lab_user = prompt_for_lab_user()

    # ── Generate employee dataset from last name ──────────────────────────────
    employees = generate_employee_dataset(lab_user)

    # ── Print dataset summary ─────────────────────────────────────────────────
    print()
    print(f"  🔑 Lab namespace  : {lab_user}")
    print(f"  📂 Output folder  : HR_{lab_user}/")
    print(f"  🗂️  Repository path: /BOB_LAB/{lab_user}/")
    print()
    print("  Your employees for this lab:")
    print(f"  {'#':<4} {'ID':<10} {'Name':<22} {'Department':<20} {'Role'}")
    print("  " + "─" * 80)
    for i, emp in enumerate(employees, 1):
        print(f"  {i:<4} {emp['id']:<10} {emp['name']:<22} {emp['department']:<20} {emp['position']}")
    print()

    # ── Validate employee filter ──────────────────────────────────────────────
    filter_employee_id = None
    if args.employee is not None:
        if args.employee < 1 or args.employee > len(employees):
            print(f"  Error: --employee index must be between 1 and {len(employees)}.")
            sys.exit(1)
        filter_employee_id = employees[args.employee - 1]["id"]

    # ── Run generation ────────────────────────────────────────────────────────
    total_files, total_seeded = generate_all_documents(
        employees=employees,
        seed_misclassifications=args.seed_misclassifications,
        dry_run=args.dry_run,
        filter_employee=filter_employee_id,
        lab_user=lab_user,
    )

    if not args.dry_run:
        print("Next steps:")
        if args.seed_misclassifications:
            print(f"  1. Open Lab2_Generate_Sample_Content.md and follow Scene 3-4 to upload documents.")
            print(f"  2. Tell Bob: 'Upload HR documents from HR_{lab_user}/ — my namespace is {lab_user}'")
            print(f"  3. After upload, proceed to Lab3_Review_and_Reclassify.md.")
            print(f"  4. Bob will need to find and fix {total_seeded} misclassified documents in /BOB_LAB/{lab_user}/")
        else:
            print(f"  1. Open Lab2_Generate_Sample_Content.md and follow Scene 3-4 to upload documents.")
            print(f"  2. Tell Bob: 'Upload HR documents from HR_{lab_user}/ — my namespace is {lab_user}'")


if __name__ == "__main__":
    main()

# Made with Bob
