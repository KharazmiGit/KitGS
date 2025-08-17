from . import views
from django.urls import path

app_name = 'account_app'
urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    path('register/gam/user', views.RegisterGamUserC.as_view(), name='register_gam_user'),
]
