from main.models import *

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.amount * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):
    DELIVERY_CHOICES = (
        ('Standard', 'Standard'),
        ('Fast', 'Fast')
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Delivering', 'Delivering'),
        ('Completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    delivery_type = models.CharField(max_length=255, choices=DELIVERY_CHOICES)
    payment_type = models.CharField(max_length=255, default='CASH')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    total_price = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    created_at = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

    def calculate_total_price(self):
        pass

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.user.username} - {self.product.name}"