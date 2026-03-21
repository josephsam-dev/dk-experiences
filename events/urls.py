from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.events_page, name='events'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('buy-ticket/<int:id>/', views.buy_ticket, name='buy_ticket'),
]