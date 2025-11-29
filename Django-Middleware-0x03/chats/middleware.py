from datetime import datetime
import time
from django.http import JsonResponse

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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store requests per IP:  {ip: [timestamps]}
        self.requests_log = {}

        # Configuration
        self.MAX_REQUESTS = 5          # 5 messages allowed
        self.TIME_WINDOW = 60          # per minute (60 seconds)

    def __call__(self, request):
        # We only rate-limit chat messages, assuming they are POST requests
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize list for new IP
            if ip not in self.requests_log:
                self.requests_log[ip] = []

            # Filter timestamps: keep only those within the last 60 seconds
            self.requests_log[ip] = [
                ts for ts in self.requests_log[ip]
                if now - ts <= self.TIME_WINDOW
            ]

            # If limit exceeded, block request
            if len(self.requests_log[ip]) >= self.MAX_REQUESTS:
                return JsonResponse(
                    {"error": "Message limit exceeded. Try again in 1 minute."},
                    status=429
                )

            # Otherwise, log this request timestamp
            self.requests_log[ip].append(now)

        # Continue to view
        return self.get_response(request)

    def get_client_ip(self, request):
        """Get user IP address safely."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
