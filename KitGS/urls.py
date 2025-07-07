from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scraper/', include('scraper.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/',include('core.urls'))
]
