from django.contrib import admin
from .models import Event, Ticket


# ✅ EVENT ADMIN
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "date", "time", "price")
    search_fields = ("title", "location")
    list_filter = ("date",)


# ✅ TICKET ADMIN (UPGRADED 🔥)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "total_amount", "reference")
    search_fields = ("email", "reference")
    readonly_fields = ("reference",)

# ✅ REGISTER
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)