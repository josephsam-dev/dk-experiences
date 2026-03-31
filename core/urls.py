<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('events/', views.events, name='events'),

     path("travel/", include("travel.urls")),
]
    


# ✅ MEDIA (uploads)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 🔥 ADD THIS (THIS IS THE FIX)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    
=======
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),

    path('blog/', views.blog, name='blog'),  # ✅ ADD THIS
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
]
>>>>>>> 2ac0cf1 (fresh clean commit without secrets)
