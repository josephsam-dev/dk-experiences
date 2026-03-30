from django.contrib import admin
from .models import TravelPackage, Booking, BlogPost, PartnershipApplication, Ticket, TicketType

admin.site.register(TravelPackage)
admin.site.register(Booking)
admin.site.register(BlogPost)
admin.site.register(PartnershipApplication)
admin.site.register(Ticket)
admin.site.register(TicketType)