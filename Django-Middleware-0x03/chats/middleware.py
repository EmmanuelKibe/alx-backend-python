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