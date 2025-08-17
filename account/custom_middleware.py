from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    """
    Custom middleware that:
    1. Redirects unauthenticated users to the login page.
    2. Redirects 404s (page not found) to the landing page.
    """

    def process_request(self, request):
        # Allow all admin URLs and static/media
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/media'):
            return None

        try:
            # Try to resolve the current URL into a view
            match = resolve(request.path_info)
            view_name = f"{match.app_name}:{match.url_name}" if match.app_name else match.url_name
        except Resolver404:
            # Let process_response handle 404
            return None

        # Views that don't require authentication
        exempt_views = [
            'account_app:login',
            'account_app:logout',
            'core_app:landing-page',
        ]

        # If user is not logged in and trying to access a protected view → redirect to login
        if not request.user.is_authenticated and view_name not in exempt_views:
            return redirect('account_app:login')

        return None  # allow normal flow

    def process_response(self, request, response):
        # Redirect all 404s to landing page
        if response.status_code == 404:
            return redirect('core_app:landing-page')
        return response
