# your_app/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path in [reverse('login'), reverse('signup')]:
            return redirect('home')  # Replace 'home' with the URL name of the page to redirect to
        response = self.get_response(request)
        return response
