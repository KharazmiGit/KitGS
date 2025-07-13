from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        exempt_paths = [
            '/accounts/login',
            '/accounts/logout',
            '/landing',
        ]

        # Get the base path without query parameters
        base_path = request.path.split('?')[0]

        print(f"\nMiddleware Debug:")
        print(f"Path: {base_path}")
        print(f"Authenticated: {request.user.is_authenticated}")

        if request.user.is_authenticated : 
            print("we are tracking the user")
        elif not any(base_path == path or base_path == path + '/' for path in exempt_paths):
            print('Not redirecting - not authenticated')
            return redirect('core_app:landing-page')
