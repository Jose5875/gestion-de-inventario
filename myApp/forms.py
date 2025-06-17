from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product,Customer, Category, Sale, Sales_Details, Employee, Inventory, Supplier, User, Expense

class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'amount', 'supplier', 'category' ]
        labels = {
            'name': 'Nombre del Producto',
            'price': 'Precio Unitario',
            'amount': 'Cantidad Disponible',
            'supplier': 'Provedor',
            'category': 'Tipo de Producto',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier' : forms.Select(attrs={'class': 'form-select'}),
            'category' : forms.Select(attrs={'class': 'form-select'}),
        }

class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'gmail', 'phone', 'address']
        labels = {
            'name': 'Nombre del Cliente',
            'gmail': 'Correo Electrónico',
            'phone': 'Teléfono de Contacto',
            'address': 'Dirección del Cliente',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'gmail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3}),
        }

class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
        }

class saleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'employee']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el cliente'}),
            'employee': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el empleado'}),
        }

class salesDetailForm(forms.ModelForm):
    class Meta:
        model = Sales_Details
        fields = ['producto', 'amount', 'unit_price']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el producto'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio unitario', 'step': '0.01'}),
        }

class employeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'gmail', 'phone', 'post']
        labels = {
            'name': 'Nombre del Empleado',
            'gmail': 'Correo Electrónico',
            'phone': 'Teléfono de Contacto',
            'post': 'Cargo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del empleado'}),
            'gmail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'post': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo del empleado'}),
        }

class supplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'company', 'gmail', 'phone', 'address']
        labels = {
            'name': 'Nombre del Proveedor',
            'company': 'Nombre de la Empresa',
            'gmail': 'Correo Electrónico',
            'phone': 'Teléfono de Contacto',
            'address': 'Dirección',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'gmail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3}),
        }

class RestockForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad a agregar'
        })
    )
    reason = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Razón del reabastecimiento'
        })
    )

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    phone = forms.CharField(max_length=20, required=True, label='Teléfono')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label= 'Usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label= 'Contraseña')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto del gasto', 'step': '0.01', 'min': '0'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del gasto'}),
        }
