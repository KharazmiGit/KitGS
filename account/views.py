from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


@method_decorator([never_cache, csrf_protect], name='dispatch')
class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core_app:landing-page')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        remember_me = request.POST.get('remember') == 'on'

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                # Set session to expire when browser closes
                request.session.set_expiry(0)
            return redirect('core_app:landing-page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('account_app:login')


@method_decorator(login_required, name='dispatch')
class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('account_app:login')
