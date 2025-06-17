from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that should be accessible without login
        allowed_paths = [
            reverse('login'),
            reverse('customerregistration'),
            reverse('password_reset'),  # Changed from password-reset to password_reset
            '/admin/',
            '/static/',
            '/media/',
        ]

        if not request.user.is_authenticated:
            # Check if the current path is not in allowed_paths
            if not any(request.path.startswith(path) for path in allowed_paths):
                return redirect('login')

        response = self.get_response(request)
        return response
