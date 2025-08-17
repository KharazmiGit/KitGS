from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from . import models
from time import sleep

@method_decorator([never_cache, csrf_protect], name='dispatch')
class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core_app:landing-page')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('uname')
        password = request.POST.get('psw')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core_app:landing-page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('account_app:login')


@method_decorator(login_required, name='dispatch')
class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('account_app:login')


class RegisterGamUserC(View):
    def get(self, request):
        return render(request, 'register_gam_user.html')

    def post(self, request):
        username = request.POST.get('username')
        ip = request.POST.get('ip')
        password = request.POST.get('password')

        # Basic validation
        if not (username and ip and password):
            messages.error(request, "All fields are required.")
            return render(request, 'register_gam_user.html', {'request': request})

        # Check for existing user
        if models.GamAccount.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register_gam_user.html', {'request': request})

        # Create and save user
        new_user = models.GamAccount(username=username, desktop_ip=ip, gam_password=password)
        new_user.save()

        messages.success(request, "Registration successful.")
        sleep(3)
        return redirect('account_app:register_gam_user')
