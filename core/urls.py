from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('travel/', include('travel.urls')),
    path('contact/', views.contact, name='contact'),
    
]

    
