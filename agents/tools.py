from langchain_core.tools import Tool

def get_leave_balance(user_id: str) -> str:
    return "You have 8 leave days remaining."

def submit_leave_request(date: str, reason: str) -> str:
    return f"Leave request for {date} ({reason}) submitted!"

def lookup_policy(topic: str) -> str:
    return f"Policy for {topic}: [Mock policy details here]"

def escalate_to_hr(human_request: str) -> str:
    return "Your request has been escalated to HR. Someone will contact you soon."

def calendar_api(query: str) -> str:
    return "Next company holiday is on July 4th."

tools = [
    Tool(name="GetLeaveBalance", func=get_leave_balance, description="Check remaining leave days for a user."),
    Tool(name="SubmitLeaveRequest", func=submit_leave_request, description="Submit a leave request."),
    Tool(name="LookupPolicy", func=lookup_policy, description="Look up HR policy details."),
    Tool(name="EscalateToHR", func=escalate_to_hr, description="Escalate complex queries to a human HR rep."),
    Tool(name="CalendarAPI", func=calendar_api, description="Check company holidays and events."),
] 