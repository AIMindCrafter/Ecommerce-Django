from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that should be accessible without login
        # Allow the home page exactly, but not as a prefix (so only "/" is allowed exactly)
        allowed_exact = {
            reverse('home'),  # typically '/'
        }

        # Paths allowed by prefix matching
        allowed_prefixes = [
            reverse('login'),
            reverse('customerregistration'),
            reverse('password_reset'),  # '/password-reset/'
            '/admin/',
            '/static/',
            '/media/',
        ]

        if not request.user.is_authenticated:
            # Allow if exact match to home, or starts with one of the allowed prefixes
            if not (request.path in allowed_exact or any(request.path.startswith(path) for path in allowed_prefixes)):
                return redirect('login')

        response = self.get_response(request)
        return response
