from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('TSHIRT', 'Футболки'),
        ('HOODIE', 'Худі'),
        ('SHORTS', 'Шорти'),
        ('SCARF', 'Шарфи'),
        ('SOUVENIR', 'Сувеніри'),
        ('OTHER', 'Інше'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    has_sizes = models.BooleanField(default=False, verbose_name="Є розміри?")
    has_colors = models.BooleanField(default=False, verbose_name="Є кольори?")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('completed', 'Виконано'),
        ('canceled', 'Скасовано'),
    ]
    DELIVERY_CHOICES = [
        ('nova_poshta', 'Нова Пошта'),
        ('ukr_poshta', 'Укрпошта'),
        ('pickup', 'Самовивіз'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'Оплата карткою (Visa/Mastercard)'),
        ('cod', 'Оплата при отриманні'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='nova_poshta')

    # Оновлені поля для адреси
    city = models.CharField(max_length=100, blank=True, null=True)
    warehouse = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)  # Для Укрпошти або самовивозу

    comment = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        if not self.price or not self.quantity:
            return 0
        return self.price * self.quantity