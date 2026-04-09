from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # or wherever your contact view is

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('events/', include('events.urls')),
    path('travel/', include('travel.urls')),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)