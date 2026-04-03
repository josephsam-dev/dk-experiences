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
class Ticket(models.Model):
    category = models.CharField(max_length=100)
    event = models.ForeignKey(
    Event,
    on_delete=models.CASCADE,
    related_name="tickets"
)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    payment_reference = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.event.title}"


# ✅ TRAVEL
class TravelPackage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='travel/')

    def __str__(self):
        return self.title