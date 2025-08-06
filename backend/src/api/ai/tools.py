# tools.py
from langchain_core.tools import tool
from api.my_emailer.sender import send_mail
from api.my_emailer.inbox_reader import read_inbox
from api.ai.services import generate_email_message


@tool
def research_email(query:str):
    """
    Perform research based on the query 

    Args:
        query (str): Topic of research
    """
    response = generate_email_message(query)
    msg = f"Subject {response.subject}:\nBody: {response.content}"
    return msg



@tool
def send_me_email(subject:str, content:str):
    """
    Send an email to myself with a subject and content.

    Args:
        subject (str): Text subject of the email
        content (str): Text body of the email
    """

    try:
        send_mail(subject=subject, content=content)
    except:
        return "Not sent"
    return "Sent mail"

@tool
def get_unread_emails(hours_ago:int=48):
    """
    Read all emails from my indox within the last N hours

    Args:
        hours_ago (int): Number of hours ago to retrieve in the inbox
    
    Returns:
        A string of emails separated by a line "----"
    """

    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except:
        return "Error getting latest emails"
    cleaned = []
    for email in emails:
        print(email)
        data = email.copy()
        if "html_body" in data:
            data.pop("html_body")
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t{v}"
        cleaned.append(msg)
    return "\n-------\n".join(cleaned)[:100]