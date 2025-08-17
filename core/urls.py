from django.urls import path
from . import views

app_name = 'core_app'
urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing-page'),
]
