from langchain_core.tools import Tool
import datetime
import re

# Company holiday calendar
COMPANY_HOLIDAYS = [
    {"date": "2025-01-01", "name": "New Year"},
    {"date": "2025-05-26", "name": "Memorial Day"},
    {"date": "2025-07-04", "name": "Independence Day"},
    {"date": "2025-09-01", "name": "Labor Day"},
    {"date": "2025-11-27", "name": "Thanksgiving"},
    {"date": "2025-11-28", "name": "Day after Thanksgiving"},
    {"date": "2025-12-25", "name": "Christmas"},
    # Plus three floating holidays
]

# Employee benefits information
def get_benefits_info(query: str) -> str:
    query_lower = query.lower()
    if "health" in query_lower or "medical" in query_lower:
        return (
            "Health Benefits: We offer comprehensive medical, dental, and vision coverage. "
            "Premium plans include PPO and HMO options with low deductibles. "
            "Annual enrollment period is October 1-31. Contact benefits@companyname.com for details."
        )
    elif "retirement" in query_lower or "401k" in query_lower:
        return (
            "Retirement Benefits: 401(k) plan with 6% company match, immediate vesting. "
            "Also includes traditional and Roth IRA options. "
            "Financial planning resources available through Fidelity."
        )
    elif "pto" in query_lower or "vacation" in query_lower:
        return (
            "PTO Policy: Unlimited PTO for full-time employees. "
            "Minimum 3 weeks recommended annually. Manager approval required for 5+ consecutive days. "
            "Public holidays are separate from PTO."
        )
    else:
        return (
            "Available benefits: Health/Medical, Dental, Vision, 401(k), Life Insurance, "
            "Disability Coverage, Flexible Spending Account, Employee Assistance Program, "
            "Professional Development Budget. Ask about specific benefits for details."
        )

# Employee onboarding assistance
def get_onboarding_info(query: str) -> str:
    query_lower = query.lower()
    if "first day" in query_lower or "start" in query_lower:
        return (
            "First Day: Report to reception at 9 AM with ID and completed paperwork. "
            "You'll receive laptop, badge, and office tour. "
            "Lunch will be provided. Orientation sessions run until 4 PM."
        )
    elif "paperwork" in query_lower or "documents" in query_lower:
        return (
            "Required Documents: I-9 form, tax forms (W-4), direct deposit form, "
            "emergency contacts, benefits enrollment forms. "
            "Most forms are available in the employee portal: portal.companyname.com"
        )
    elif "equipment" in query_lower or "laptop" in query_lower:
        return (
            "Equipment Setup: Laptop, monitor, keyboard, mouse provided on first day. "
            "IT will help with software installation and account setup. "
            "Mobile phone provided if role requires. Contact it-support@companyname.com"
        )
    elif "training" in query_lower:
        return (
            "Training Schedule: Week 1 - Company orientation and compliance training. "
            "Week 2 - Role-specific training with your manager. "
            "Week 3-4 - Department integration and project assignments. "
            "Learning management system: learn.companyname.com"
        )
    else:
        return (
            "Onboarding Support: First day logistics, required paperwork, equipment setup, "
            "training schedule, mentor assignment. Ask about specific onboarding topics for details."
        )

# Performance review information
def get_performance_info(query: str) -> str:
    query_lower = query.lower()
    if "schedule" in query_lower or "when" in query_lower:
        return (
            "Performance Review Schedule: Annual reviews in Q1 (January-March). "
            "Mid-year check-ins in July. Quarterly 1:1s with manager. "
            "30/60/90 day reviews for new hires."
        )
    elif "process" in query_lower or "how" in query_lower:
        return (
            "Review Process: Self-assessment, manager evaluation, peer feedback (360 review). "
            "Goal setting for upcoming year. Performance rating scale: Exceeds/Meets/Below Expectations. "
            "Results discussion meeting within 2 weeks of completion."
        )
    elif "goals" in query_lower or "objectives" in query_lower:
        return (
            "Goal Setting: SMART goals framework (Specific, Measurable, Achievable, Relevant, Time-bound). "
            "3-5 key objectives per year. Quarterly progress reviews. "
            "Career development goals included. Use goals.companyname.com"
        )
    elif "feedback" in query_lower:
        return (
            "Feedback Culture: Continuous feedback encouraged. Anonymous feedback tool available. "
            "Regular 1:1s with manager. Peer recognition program. "
            "Open door policy for performance concerns."
        )
    else:
        return (
            "Performance Management: Annual reviews, goal setting, feedback processes, "
            "career development, promotion criteria. Ask about specific performance topics for details."
        )

# Employee leave balance information
def get_leave_balance(user_id: str) -> str:
    return (
        "To check your leave balance, log in to the HR portal at hr.companyname.com, "
        "navigate to: My Profile > Time Off > Leave Balance. You will see a breakdown of Earned Leave (EL), Casual Leave (CL), Sick Leave (SL), and carry-forward balances. "
        "If you have questions, contact hr-support@companyname.com."
    )

def calendar_api(query: str) -> str:
    query_lower = query.lower()
    if "next" in query_lower and "holiday" in query_lower:
        today = datetime.datetime.now()
        for holiday in COMPANY_HOLIDAYS:
            holiday_date = datetime.datetime.strptime(holiday["date"], "%Y-%m-%d")
            if holiday_date > today:
                days_until = (holiday_date - today).days
                return f"Next holiday: {holiday['name']} on {holiday['date']} (in {days_until} days)"
    elif "all" in query_lower or "list" in query_lower:
        holiday_list = "\n".join([f"- {h['name']}: {h['date']}" for h in COMPANY_HOLIDAYS])
        return f"All company holidays in 2025:\n{holiday_list}\nPlus three floating holidays."
    elif "holiday" in query_lower:
        return f"Company holidays include: {', '.join([h['name'] for h in COMPANY_HOLIDAYS])}, plus three floating holidays."
    return "Calendar information not found. Try asking about 'holidays' or 'next holiday'."

# HR directory/contact lookup
def get_hr_directory(query: str) -> str:
    query_lower = query.lower()
    contacts = {
        "hr": "hr-support@companyname.com | Phone: (555) 123-4567 | Office: Building A, Floor 3",
        "payroll": "payroll@companyname.com | Phone: (555) 123-4568 | Processing dates: 15th and 30th",
        "benefits": "benefits@companyname.com | Phone: (555) 123-4569 | Open enrollment: Oct 1-31",
        "it": "it-support@companyname.com | Phone: (555) 123-4570 | Help desk hours: 8 AM - 6 PM",
        "facilities": "facilities@companyname.com | Phone: (555) 123-4571 | Building maintenance requests",
        "learning": "learning@companyname.com | Phone: (555) 123-4572 | Training and development"
    }
    
    for dept, info in contacts.items():
        if dept in query_lower:
            return f"{dept.upper()} Contact: {info}"
    
    return (
        "HR Directory - Main contacts:\n" +
        "\n".join([f"• {dept.upper()}: {info}" for dept, info in contacts.items()])
    )

# Employee handbook/policy lookup
def get_policy_info(query: str) -> str:
    query_lower = query.lower()
    policies = {
        "dress code": "Business casual. Jeans allowed on Fridays. No offensive clothing. Remote work: professional on video calls.",
        "remote work": "Hybrid policy: 2-3 days in office, 2-3 days remote. Manager approval required. Core hours: 10 AM - 3 PM.",
        "expense": "Use Expensify app. Receipts required for amounts >$25. Meals: $50/day limit. Travel pre-approval needed.",
        "time off": "Submit requests 2 weeks in advance. Manager approval required. No PTO during month-end close periods.",
        "overtime": "Non-exempt employees: OT approved in advance. Rate: 1.5x regular pay. Comp time available for exempt staff.",
        "social media": "Personal accounts: don't mention company. Professional accounts: follow brand guidelines. No confidential info.",
        "discrimination": "Zero tolerance for discrimination based on protected grounds: Indigenous identity, race, colour, ancestry, place of origin, religion, family status, marital status, physical/mental disability, sex, age, sexual orientation, gender identity/expression, political belief, or criminal conviction unrelated to employment. Report violations to supervisor or HR immediately.",
        "harassment": "Workplace free from harassment including inappropriate conduct causing humiliation or intimidation. Includes verbal aggression, derogatory names, malicious rumors, inappropriate materials, unwelcome sexual remarks. Report incidents to supervisor, next level management, or HR.",
        "bullying": "Bullying includes conduct causing humiliation/intimidation, repeated behavior affecting well-being, or single serious incidents with lasting harmful effects. May be written, verbal, physical, online, or electronic. Excludes reasonable management direction.",
        "workplace conduct": "All employees must treat others with respect and dignity. Conduct must meet acceptable social standards and contribute to positive work environment. Standards of Conduct must be followed at all times.",
        "reporting procedure": "Step 1: Seek advice from supervisor, manager, or union. Step 2: Try informal resolution if safe. Step 3: Formal report to supervisor or excluded management. Step 4: Investigation and corrective action. Confidentiality maintained throughout process."
    }
    
    for policy, details in policies.items():
        if policy in query_lower or any(word in query_lower for word in policy.split()):
            return f"{policy.title()} Policy: {details}"
    
    return (
        "Available policies: Dress Code, Remote Work, Expense Reporting, Time Off, " +
        "Overtime, Social Media, Discrimination, Harassment, Bullying, Workplace Conduct, Reporting Procedure. Ask about a specific policy for details."
    )

# Salary and compensation information
def get_compensation_info(query: str) -> str:
    query_lower = query.lower()
    if "pay" in query_lower or "salary" in query_lower:
        return (
            "Salary Information: Pay reviews annually in March. " +
            "Merit increases based on performance. Market adjustments considered. " +
            "Salary bands available from your manager. Questions: payroll@companyname.com"
        )
    elif "bonus" in query_lower:
        return (
            "Bonus Structure: Annual performance bonus (0-20% of salary). " +
            "Spot bonuses for exceptional work. Referral bonuses: $2,500 for successful hires. " +
            "Paid in March with annual reviews."
        )
    elif "raise" in query_lower or "promotion" in query_lower:
        return (
            "Promotion Process: Annual review cycle, merit-based increases. " +
            "Career ladder framework available. Internal mobility encouraged. " +
            "Discuss career goals with manager during 1:1s."
        )
    else:
        return (
            "Compensation Topics: Salary information, bonus structure, promotion process, " +
            "pay equity, market adjustments. Ask about specific compensation topics."
        )

# Workplace safety and incident reporting
def get_safety_info(query: str) -> str:
    query_lower = query.lower()
    if "incident" in query_lower or "report" in query_lower:
        return (
            "Incident Reporting: Report workplace incidents immediately to supervisor and HR. "
            "Use incident report form available on intranet. For discrimination, bullying, or harassment: "
            "Contact supervisor, next level management, or hr-support@companyname.com. "
            "Anonymous reporting available through ethics hotline: 1-800-ETHICS."
        )
    elif "safety" in query_lower or "emergency" in query_lower:
        return (
            "Workplace Safety: Emergency exits marked with red signs. Fire extinguishers on each floor. "
            "Emergency contact: Call 911. Building security: (555) 123-4571. "
            "First aid kits located in break rooms. Report unsafe conditions immediately."
        )
    elif "discrimination" in query_lower or "harassment" in query_lower or "bullying" in query_lower:
        return (
            "Discrimination/Harassment/Bullying Reporting: Multiple reporting options available: "
            "1) Direct supervisor or next level management, 2) HR department at hr-support@companyname.com, "
            "3) Anonymous ethics hotline: 1-800-ETHICS, 4) Union representative if applicable. "
            "Protection from reprisal guaranteed. Confidentiality maintained throughout investigation process."
        )
    else:
        return (
            "Safety Resources: Incident reporting procedures, emergency protocols, "
            "discrimination/harassment reporting, workplace safety guidelines. "
            "Ask about specific safety topics for details."
        )

tools = [
    Tool(name="GetLeaveBalance", func=get_leave_balance, description="How to check your leave balance. Input: employee ID (e.g., user123)"),
    Tool(name="CalendarAPI", func=calendar_api, description="Check company holidays and events. Input: query about holidays or calendar"),
    Tool(name="BenefitsInfo", func=get_benefits_info, description="Get information about employee benefits (health, retirement, PTO, etc.). Input: benefits query"),
    Tool(name="OnboardingInfo", func=get_onboarding_info, description="Get onboarding information for new employees (first day, paperwork, equipment, training). Input: onboarding query"),
    Tool(name="PerformanceInfo", func=get_performance_info, description="Get information about performance reviews, goals, and feedback processes. Input: performance query"),
    Tool(name="HRDirectory", func=get_hr_directory, description="Get HR department contact information and directory. Input: department or contact query"),
    Tool(name="PolicyInfo", func=get_policy_info, description="Get company policy information including discrimination, harassment, bullying, workplace conduct, and reporting procedures. Input: policy query"),
    Tool(name="CompensationInfo", func=get_compensation_info, description="Get information about salary, bonuses, promotions, and compensation. Input: compensation query"),
    Tool(name="SafetyInfo", func=get_safety_info, description="Get workplace safety information, incident reporting procedures, and discrimination/harassment reporting options. Input: safety or incident query"),
] 