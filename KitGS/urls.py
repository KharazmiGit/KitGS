from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scraper/', include('scraper.urls')),
    path('accounts/', include('account.urls')),
    path('/', include('core.urls'))
]