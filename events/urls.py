from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('events/', views.events_page, name='events'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('buy-ticket/<int:id>/', views.buy_ticket, name='buy_ticket'),
=======
    path('', views.events, name='events'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('buy-ticket/<int:id>/', views.buy_ticket, name='buy_ticket'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('blog/', views.blog, name='blog'),
>>>>>>> 2ac0cf1 (fresh clean commit without secrets)
]