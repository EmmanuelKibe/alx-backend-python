from datetime import datetime

class RequestLoggingMiddleware:
    """
    Middleware that logs each incoming request's method and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the authenticated user, or "AnonymousUser"
        user = request.user if request.user.is_authenticated else "AnonymousUser"

        # Format the log message
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Append log to file
        with open("request_logs.txt", "a") as log_file:
            log_file.write(log_message)

        # Continue processing the request
        response = self.get_response(request)

        return response
    
class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access outside 9pm and 6am.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access is restricted between 9 PM and 6 AM.")

        response = self.get_response(request)
        return response