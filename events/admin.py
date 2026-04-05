from django.contrib import admin
from .models import Event, Ticket
from django.db.models import Sum


# =========================
# ✅ EVENT ADMIN
# =========================
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "date", "time", "price")
    search_fields = ("title", "location")
    list_filter = ("date",)


# =========================
# ✅ TICKET ADMIN + DASHBOARD 🔥
# =========================
class TicketAdmin(admin.ModelAdmin):
    change_list_template = "admin/ticket_change_list.html"

    list_display = (
        "email",
        "phone",
        "total_amount",
        "paid",
        "used",
        "reference",
        "created_at",
    )

    search_fields = ("email", "reference")
    readonly_fields = ("reference",)
    list_filter = ("paid", "used")

    def changelist_view(self, request, extra_context=None):
        total_paid = Ticket.objects.filter(paid=True).count()
        total_revenue = Ticket.objects.filter(paid=True).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        extra_context = extra_context or {}
        extra_context["total_paid"] = total_paid
        extra_context["total_revenue"] = total_revenue

        return super().changelist_view(request, extra_context=extra_context)


# =========================
# ✅ REGISTER MODELS
# =========================
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)