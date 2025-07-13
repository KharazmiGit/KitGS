from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        exempt_paths = [
            '/accounts/login',
            '/accounts/logout',
            '/landing',
            '/admin',
        ]

        # Get the base path without query parameters
        base_path = request.path.split('?')[0]

        print(f"\nMiddleware Debug:")
        print(f"Path: {base_path}")
        print(f"Authenticated: {request.user.is_authenticated}")

        if request.user.is_authenticated:
            # Only allow exact matches for exempt paths
            if not any(base_path == path or base_path == path + '/' for path in exempt_paths):
                print('Redirecting to landing page')
                return redirect('core_app:landing-page')
            else:
                print('Not redirecting - exact path match')
        else:
            print('Not redirecting - not authenticated')