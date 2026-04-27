from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from pydantic import BaseModel, Field

class JiraTicketInput(BaseModel):
    summary: str = Field(description="A short and brief title of the problem in spanish (e.g: Falla de internet en Bogotá)")
    description: str = Field(description="Detailed explanation of the problem, including the CC of the user and the steps that were tried")



@tool("create_jira_incident", args_schema=JiraTicketInput)
def create_jira_incident(summary, description):
    """
    Use this tool when the problem vould not be resolved via chat and it persists, you will have to summarize the problem
    brieffly and provide a full description of the problem DO NOT INCLUDE personal information such as name and email, just include the CC or ID of the user, you will have 
    to include the necessary data collected and the MAC address of the user
    """
    load_dotenv() 
    email = os.getenv("EMAIL")
    api_key = os.getenv("JIRA_API_KEY")
    domain = os.getenv("JIRA_DOMAIN")
    url = f"https://{domain}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, api_key) # type: ignore
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "fields": {
            "project": {
                "key": "SUP"
            },
            "summary": summary,
            "issuetype": {
                "name": "[System] Incident"
            },
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            { "text": description, "type": "text" }
                        ]
                    }
                ]
            }
        }
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

