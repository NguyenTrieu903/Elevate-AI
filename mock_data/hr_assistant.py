"""HR Assistant mock data for RAG chatbot system."""

from typing import List, Dict, Any
from datetime import datetime, timedelta

# HR Assistant FAQ Documents
HR_ASSISTANT_DOCS = [
    {
        "page_content": "How to request time off? Log into the HR portal at hr.company.com, go to 'Time Off Requests', select leave type (vacation, sick, personal), choose dates, and submit. Manager approval required for requests over 3 days. Submit at least 2 weeks in advance for vacation requests.",
        "metadata": {"source": "FAQ - Time Off Requests", "category": "Leave Management", "priority": "high"}
    },
    {
        "page_content": "Employee onboarding checklist: Complete I-9 form with HR, set up direct deposit, enroll in benefits (health, dental, 401k), attend orientation session, receive IT equipment, complete required training modules, and schedule meeting with manager for role expectations.",
        "metadata": {"source": "FAQ - Onboarding Process", "category": "Onboarding", "priority": "high"}
    },
    {
        "page_content": "Benefits enrollment information: Open enrollment period is November 1-30. Choose health insurance plan (PPO, HMO options available), dental and vision coverage, life insurance, and 401k contribution percentage. Changes allowed only during open enrollment or qualifying life events.",
        "metadata": {"source": "FAQ - Benefits Enrollment", "category": "Benefits", "priority": "medium"}
    },
    {
        "page_content": "Performance review process: Annual reviews conducted in January. Self-evaluation due by December 15. Manager review and goal setting in January. Mid-year check-ins scheduled for July. Use SMART goals format. Career development discussions included in review process.",
        "metadata": {"source": "FAQ - Performance Reviews", "category": "Performance", "priority": "medium"}
    },
    {
        "page_content": "Payroll and salary information: Payday is every other Friday. Access pay stubs through HR portal. Direct deposit setup required. Tax withholding changes can be made anytime via W-4 form. Year-end W-2 forms available by January 31st in HR portal.",
        "metadata": {"source": "FAQ - Payroll Information", "category": "Payroll", "priority": "medium"}
    },
    {
        "page_content": "Company policies and handbook: Employee handbook available on company intranet. Covers code of conduct, dress code, remote work policy, anti-harassment policy, and disciplinary procedures. All employees must acknowledge receipt annually. Updates communicated via email.",
        "metadata": {"source": "FAQ - Company Policies", "category": "Policies", "priority": "low"}
    },
    {
        "page_content": "Training and development opportunities: Required compliance training due annually. Professional development budget $1000/year per employee. Request approval for conferences, courses, certifications. Internal mentorship program available. Leadership development track for senior roles.",
        "metadata": {"source": "FAQ - Training & Development", "category": "Training", "priority": "medium"}
    },
    {
        "page_content": "Remote work policy: Hybrid schedule allowed (minimum 2 days in office). Full remote work requires manager approval and business justification. Home office stipend $500/year. VPN access required. Regular check-ins with team mandatory.",
        "metadata": {"source": "FAQ - Remote Work Policy", "category": "Remote Work", "priority": "high"}
    },
    {
        "page_content": "Health and safety protocols: Report workplace injuries immediately to supervisor and HR. First aid stations located on each floor. Emergency evacuation procedures posted. COVID-19 protocols: stay home if sick, masks optional, sanitization stations available.",
        "metadata": {"source": "FAQ - Health & Safety", "category": "Safety", "priority": "medium"}
    },
    {
        "page_content": "Employee referral program: Refer qualified candidates for open positions. $1000 bonus for successful hires (paid after 90 days). Submit referrals through HR portal. Referrer and candidate must meet eligibility criteria. Cannot refer family members.",
        "metadata": {"source": "FAQ - Employee Referrals", "category": "Referrals", "priority": "low"}
    }
]

# Employee Leave Balances (mock data)
EMPLOYEE_LEAVE_BALANCES = {
    "EMP001": {
        "name": "John Smith",
        "vacation_days": 15,
        "sick_days": 8,
        "personal_days": 3,
        "department": "Engineering"
    },
    "EMP002": {
        "name": "Sarah Johnson",
        "vacation_days": 20,
        "sick_days": 12,
        "personal_days": 5,
        "department": "Marketing"
    },
    "EMP003": {
        "name": "Mike Chen",
        "vacation_days": 12,
        "sick_days": 6,
        "personal_days": 2,
        "department": "Sales"
    }
}

# Benefits Information
BENEFITS_INFO = {
    "health_insurance": {
        "ppo_plan": {
            "monthly_premium": 150,
            "deductible": 1000,
            "coverage": "80% after deductible"
        },
        "hmo_plan": {
            "monthly_premium": 100,
            "deductible": 500,
            "coverage": "90% after deductible"
        }
    },
    "dental_insurance": {
        "monthly_premium": 25,
        "coverage": "100% preventive, 80% basic, 50% major"
    },
    "vision_insurance": {
        "monthly_premium": 10,
        "coverage": "Eye exams, glasses, contacts"
    },
    "401k": {
        "company_match": "50% up to 6% of salary",
        "vesting_schedule": "Immediate vesting",
        "maximum_contribution": "IRS limit applies"
    }
}

# Company Holidays
COMPANY_HOLIDAYS_2025 = [
    {"date": "2025-01-01", "name": "New Year's Day"},
    {"date": "2025-01-20", "name": "Martin Luther King Jr. Day"},
    {"date": "2025-02-17", "name": "Presidents' Day"},
    {"date": "2025-05-26", "name": "Memorial Day"},
    {"date": "2025-07-04", "name": "Independence Day"},
    {"date": "2025-09-01", "name": "Labor Day"},
    {"date": "2025-10-13", "name": "Columbus Day"},
    {"date": "2025-11-11", "name": "Veterans Day"},
    {"date": "2025-11-27", "name": "Thanksgiving Day"},
    {"date": "2025-11-28", "name": "Day after Thanksgiving"},
    {"date": "2025-12-25", "name": "Christmas Day"}
]

# Training Courses
TRAINING_COURSES = {
    "compliance": [
        "Sexual Harassment Prevention",
        "Data Privacy and Security",
        "Code of Conduct",
        "Anti-Money Laundering"
    ],
    "professional": [
        "Project Management Fundamentals",
        "Leadership Skills",
        "Communication Excellence",
        "Time Management"
    ],
    "technical": [
        "Software Development Best Practices",
        "Cybersecurity Awareness",
        "Microsoft Office Advanced",
        "Data Analysis with Excel"
    ]
}

def get_hr_assistant_data() -> List[Dict[str, Any]]:
    """Get all HR assistant documents."""
    return HR_ASSISTANT_DOCS

def get_leave_balance(employee_id: str) -> Dict[str, Any]:
    """Get employee leave balance by employee ID."""
    return EMPLOYEE_LEAVE_BALANCES.get(employee_id, {
        "error": "Employee not found",
        "message": "Please check your employee ID or contact HR."
    })

def get_benefits_info(benefit_type: str = None) -> Dict[str, Any]:
    """Get benefits information."""
    if benefit_type:
        return BENEFITS_INFO.get(benefit_type, {
            "error": "Benefit type not found"
        })
    return BENEFITS_INFO

def get_company_holidays(year: int = 2025) -> List[Dict[str, str]]:
    """Get company holidays for specified year."""
    if year == 2025:
        return COMPANY_HOLIDAYS_2025
    return []

def check_holiday_conflict(start_date: str, end_date: str) -> List[Dict[str, str]]:
    """Check if requested dates conflict with company holidays."""
    conflicts = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for holiday in COMPANY_HOLIDAYS_2025:
        holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
        if start <= holiday_date <= end:
            conflicts.append(holiday)

    return conflicts

def get_available_training(category: str = None) -> List[str]:
    """Get available training courses by category."""
    if category and category in TRAINING_COURSES:
        return TRAINING_COURSES[category]
    elif category:
        return []
    else:
        # Return all courses
        all_courses = []
        for courses in TRAINING_COURSES.values():
            all_courses.extend(courses)
        return all_courses
