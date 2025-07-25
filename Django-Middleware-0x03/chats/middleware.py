import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)  # You can configure this logger in settings.py

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response        

    def __call__(self, request):
        # Get the current time
        now = datetime.now().time()
         # Define restricted hours: before 6 PM or after 9 PM
        if now < time(18, 0) or now > time(21, 0):
            return HttpResponseForbidden("❌ Access denied: outside allowed hours (6PM - 9PM).")

        # Continue processing
        response = self.get_response(request)
        return response       