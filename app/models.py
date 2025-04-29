from django.db import models
import uuid

class Order(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed (e.g., customer name)

    def __str__(self):
        return str(self.unique_id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item_name} (x{self.quantity})"
