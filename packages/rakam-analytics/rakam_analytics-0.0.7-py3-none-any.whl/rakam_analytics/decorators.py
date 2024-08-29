import os
import requests
import json
from functools import wraps
from rest_framework.request import Request

def register_endpoint_event(event_type: str, name: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            # Determine if this is a class-based view (CBV) or function-based view (FBV)
            if isinstance(args[0], Request):
                # Function-based view (FBV)
                request = args[0]
                view_instance = None
                func_args = args[1:]
            else:
                # Class-based view (CBV)
                view_instance = args[0]
                request = args[1]
                func_args = args[2:]

            try:
                # Build the Data
                body = request.body.decode('utf-8')
                if not body:
                    body = {}

                event_data = {
                    "endpoint": request.path,
                    "type": event_type,
                    "name": name,
                    "content": body,
                    "company": os.getenv("ANALYTICS_COMPANY", "BASE_COMPANY"),
                    "project": os.getenv("ANALYTICS_PROJECT", "BASE_PROJECT")
                }

                # Extract headers from the incoming request
                headers = {k: v for k, v in request.headers.items()}
                headers["Content-Type"] = "application/json"

                # Rakam Analytics API event URL
                url = os.getenv("ANALYTICS_URL", None)
                if not url:
                    raise ValueError("Analytics URL not configured. Please add ANALYTICS_URL to your environment file.")

                # Call Rakam Analytics Endpoint
                response = requests.post(url=url, json=event_data, headers=headers, timeout=10)

                if response.status_code != 201:
                    raise requests.exceptions.RequestException("External service is down")

            except Exception as e:
                # Log the error or handle it as needed
                print(f"Error during analytics event logging: {e}")
            
            finally:
                # Call the original view, regardless of any errors in the above code
                if view_instance:
                    return view_func(view_instance, request, *func_args, **kwargs)
                else:
                    return view_func(request, *func_args, **kwargs)
                
        return _wrapped_view
    return decorator
