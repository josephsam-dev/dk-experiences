from django.db import models


# ✅ EVENT
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    price = models.IntegerField()
    banner = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.title


# ✅ TICKET
import uuid

class Ticket(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    ticket_data = models.TextField()  # stores multiple tickets (JSON)
    total_amount = models.IntegerField()

    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
# ✅ TRAVEL
class TravelPackage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='travel/')

    def __str__(self):
        return self.title