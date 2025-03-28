from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Добавляем сортировку по умолчанию


class ComponentOption(models.Model):
    COMPONENT_TYPES = (
        ('cpu', 'Процессор'),
        ('gpu', 'Видеокарта'),
        ('ram', 'Оперативная память'),
        ('motherboard', 'Материнская плата'),
        ('case', 'Корпус'),
        ('psu', 'Блок питания'),
        ('storage', 'Накопитель'),
        ('other', 'Другое'),
    )
    name = models.CharField(max_length=100, help_text="Название комплектующего (например, Intel i7)")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Дополнительная стоимость")
    volume = models.CharField(max_length=50, blank=True, null=True, help_text="Объем/характеристика (например, 16GB)")
    type = models.CharField(max_length=50, choices=COMPONENT_TYPES, default='other', help_text="Тип комплектующего")

    def __str__(self):
        return f"{self.name} ({self.volume})" if self.volume else self.name

    class Meta:
        ordering = ['type', 'name']  # Добавляем сортировку по умолчанию


class Product(models.Model):
    COMPONENT_TYPES = (
        ('cpu', 'Процессор'),
        ('gpu', 'Видеокарта'),
        ('ram', 'Оперативная память'),
        ('motherboard', 'Материнская плата'),
        ('case', 'Корпус'),
        ('psu', 'Блок питания'),
        ('storage', 'Накопитель'),
        ('other', 'Другое'),
    )
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Базовая цена без учета комплектующих")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    model_3d = models.FileField(upload_to='3d_models/', null=True, blank=True, help_text="3D модель в формате .glb")
    stock = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, help_text="Скидка в процентах (0-100)")
    component_type = models.CharField(max_length=50, choices=COMPONENT_TYPES, default='other')
    components = models.ManyToManyField(ComponentOption, blank=True, help_text="Доступные комплектующие")
    compatible_with = models.ManyToManyField('self', symmetrical=False, blank=True, help_text="Совместимые комплектующие")
    brand = models.CharField(max_length=100, blank=True, null=True, help_text="Бренд продукта")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Добавляем сортировку по умолчанию


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Ожидает обработки'),
        ('Shipped', 'Отправлен'),
        ('Delivered', 'Доставлен'),
        ('Cancelled', 'Отменён'),
    )
    customer_name = models.CharField(max_length=200)
    address = models.TextField()
    delivery = models.CharField(max_length=50, choices=[('standard', 'Standard'), ('express', 'Express'), ('pickup', 'Pickup')])
    comment = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.TextField(default='', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

    class Meta:
        ordering = ['-created_at']  # Добавляем сортировку по умолчанию (новые заказы сначала)