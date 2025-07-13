from django.urls import path
from . import views

app_name = 'core_app'
urlpatterns = [
    path('landing/', views.LandingPageView.as_view(), name='landing-page'),
]
