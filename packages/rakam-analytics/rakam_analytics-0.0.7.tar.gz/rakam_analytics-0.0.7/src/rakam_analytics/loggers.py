import os
import requests
import json
from rest_framework.response import Response

def log_event(event_type: str, name: str, request=None, endpoint=None, content=None, headers=None):
    """
    Logs an event to the Rakam Analytics API.

    Parameters:
    event_type (str): The type of event to log.
    name (str): The name of the event to log.
    request (Request, optional): The Django REST Framework request object.
    endpoint (str, optional): The endpoint of the event.
    content (dict, optional): The content of the event.
    headers (dict, optional): The headers for the request.xe
    """
    try:
        if request:
            try:
                event_data = {
                    "endpoint": request.path,
                    "type": event_type,
                    "name": name,
                    "content": json.loads(request.body.decode('utf-8')),
                    "company": os.getenv("ANALYTICS_COMPANY", "BASE_COMPANY"),
                    "project": os.getenv("ANALYTICS_PROJECT", "BASE_PROJECT")
                }
            except json.JSONDecodeError:
                print("Invalid JSON in request body")
                return  # Continue without breaking the function
            
            headers = {k: v for k, v in request.headers.items()}

        else:
            event_data = {
                "endpoint": endpoint,
                "type": event_type,
                "name": name,
                "content": content,
                "company": os.getenv("ANALYTICS_COMPANY", "BASE_COMPANY"),
                "project": os.getenv("ANALYTICS_PROJECT", "BASE_PROJECT")
            }
            if not headers:
                headers = {}

        url = os.getenv("ANALYTICS_URL", None)
        if not url:
            print("Analytics URL not configured. Please add ANALYTICS_URL to your environment file.")
            return  # Continue without breaking the function

        # Call Rakam Analytics Endpoint
        response = requests.post(url=url, json=event_data, headers=headers, timeout=10)
        if response.status_code != 201:
            print("External service is down")
            return  # Continue without breaking the function

        print("Event logged successfully")

    except requests.exceptions.RequestException as request_exception:
        print(f"RequestException: {request_exception}")
        return  # Continue without breaking the function

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return  # Continue without breaking the function
