from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    banner = models.ImageField(upload_to="events/")

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")

    category = models.CharField(max_length=100)   # Regular, VIP, etc
    price = models.DecimalField(max_digits=10, decimal_places=2)

    buyer_name = models.CharField(max_length=200)
    buyer_email = models.EmailField()

    quantity = models.IntegerField(default=1)

    payment_reference = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.event.title}"