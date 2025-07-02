from langchain_core.tools import Tool
import datetime

# Real holiday calendar from data_ingest/holiday_calendar.txt
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

# Minimal mock employee data for leave balance inquiry
def get_leave_balance(user_id: str) -> str:
    # In a real system, this would query a database or HR API
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

tools = [
    Tool(name="GetLeaveBalance", func=get_leave_balance, description="How to check your leave balance. Input: employee ID (e.g., user123)"),
    Tool(name="CalendarAPI", func=calendar_api, description="Check company holidays and events. Input: query about holidays or calendar"),
] 