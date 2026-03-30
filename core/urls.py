from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),

    path('blog/', views.blog, name='blog'),  # ✅ ADD THIS
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
]