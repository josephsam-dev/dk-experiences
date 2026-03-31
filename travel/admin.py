from django.contrib import admin
<<<<<<< HEAD
from .models import TravelPackage, Booking, BlogPost, PartnershipApplication, Ticket
=======
from .models import TravelPackage, Booking, BlogPost, PartnershipApplication, Ticket, TicketType
>>>>>>> 2ac0cf1 (fresh clean commit without secrets)

admin.site.register(TravelPackage)
admin.site.register(Booking)
admin.site.register(BlogPost)
admin.site.register(PartnershipApplication)
<<<<<<< HEAD
admin.site.register(Ticket)
=======
admin.site.register(Ticket)
admin.site.register(TicketType)
>>>>>>> 2ac0cf1 (fresh clean commit without secrets)
