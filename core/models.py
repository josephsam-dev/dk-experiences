from django.db import models

class Ticket(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, null=True, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    ticket_data = models.TextField()
    total_amount = models.IntegerField()

    reference = models.CharField(max_length=200)
    used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.email