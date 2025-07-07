from django.urls import path
from .views import scrape_all_users

app_name = 'scraper_app'
urlpatterns = [
    path('start/', scrape_all_users, name='scraper')
]
