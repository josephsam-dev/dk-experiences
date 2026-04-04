from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_page, name='events'),
    path('events/', views.events_page, name='events_page'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('buy-ticket/<int:id>/', views.buy_ticket, name='buy_ticket'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
]