from django.db import models
import uuid


# =========================
# ✅ EVENT MODEL
# =========================
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    price = models.IntegerField()
    banner = models.ImageField(upload_to='events/', blank=True, null=True)

    is_akoka = models.BooleanField(default=False)  # 👈 MUST BE HERE

    def __str__(self):
        return self.title


# =========================
# ✅ TICKET MODEL
# =========================
class Ticket(models.Model):
    event = models.ForeignKey(
       'events.Event',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tickets"
    )

    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    ticket_data = models.TextField()
    total_amount = models.IntegerField()

    reference = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    paid = models.BooleanField(default=False)
    used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email
    
