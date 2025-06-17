from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    gmail = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# 👨‍💼 Empleado
class Employee(models.Model):
    name = models.CharField(max_length=100)
    gmail = models.EmailField()
    phone = models.CharField(max_length=20)
    post = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.post}"


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    gmail = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company})"

class Product(models.Model):
    name= models.CharField(max_length=200)
    price = models.FloatField()
    amount = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Crear automáticamente el registro de inventario
            Inventory.objects.create(
                product=self,
                current_quantity=self.amount
            )

    def updateAmount(self, newAmount):
        self.amount = newAmount
        self.save()

    def __str__(self):
        return f"nombre: {self.name} , {self.amount}"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.date.strftime('%d/%m/%Y')}"
    
    def get_total(self):
        return sum([detalle.subtotal() for detalle in self.sales_details_set.all()])


# 🛒 Detalle de Venta
class Sales_Details(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.amount * self.unit_price


# 🧮 Inventario (opcional)
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    current_quantity = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.current_quantity} unidades"

    def update_quantity(self, new_quantity, reason="Actualización manual"):
        old_quantity = self.current_quantity
        self.current_quantity = new_quantity
        self.save()
        
        # Registrar el cambio en el historial
        InventoryHistory.objects.create(
            inventory=self,
            old_quantity=old_quantity,
            new_quantity=new_quantity,
            reason=reason
        )
        Product.objects.get(id=self.product_id).updateAmount(new_quantity)
        
            
        

class InventoryHistory(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='history')
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    reason = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory.product.name} - {self.old_quantity} → {self.new_quantity} ({self.date.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        verbose_name_plural = "Inventory History"
        ordering = ['-date']

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Especificar nombres relacionados únicos para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - ${self.amount} ({self.date:%d/%m/%Y})"