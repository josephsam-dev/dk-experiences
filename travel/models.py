import uuid
from django.db import models


# =========================
# TRAVEL PACKAGE
# =========================
class TravelPackage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="travel/")
    duration = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# =========================
# BOOKING
# =========================
class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    reference = models.CharField(max_length=20, unique=True, blank=True)

    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    travelers = models.IntegerField()
    travel_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = "DK-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.name}"


# =========================
# BLOG
# =========================
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blog/")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# CONTACT
# =========================
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# PARTNERSHIP
# =========================
class PartnershipApplication(models.Model):

    PARTNERSHIP_TYPES = [
        ('hotel', 'Hotel Partnership'),
        ('event', 'Event Collaboration'),
        ('agency', 'Travel Agency'),
        ('corporate', 'Corporate Travel'),
    ]

    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    partnership_type = models.CharField(max_length=50, choices=PARTNERSHIP_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# =========================
# TICKET
# =========================
class Ticket(models.Model):

    CATEGORY_CHOICES = [
        ("early", "Early Bird"),
        ("regular", "Regular"),
        ("vip", "VIP"),
        ("vvip", "VVIP"),
    ]

    PRICE_MAP = {
        "early": 0,
        "regular": 2500,
        "vip": 7000,
        "vvip": 17000,
    }

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    ticket_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ticket_id = models.CharField(max_length=50, unique=True, blank=True)

    payment_status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.amount = self.PRICE_MAP.get(self.ticket_type, 0)

        if not self.ticket_id:
            self.ticket_id = "DKX-" + str(uuid.uuid4())[:8]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.ticket_type}"