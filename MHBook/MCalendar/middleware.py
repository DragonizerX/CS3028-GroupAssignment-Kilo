from django.http import HttpResponseRedirect
from django.conf import settings

# Handles 404 errors by redirecting user to the login page. Handled Globally

class Handle404RedirectMiddleware:      
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return HttpResponseRedirect('/MCalendar/login/')
        return response