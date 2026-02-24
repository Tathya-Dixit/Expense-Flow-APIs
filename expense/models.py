from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Type(models.TextChoices):
    INCOME = 'IN', 'Income'
    EXPENSE = 'EX', 'Expense'

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    type_choice = models.CharField(max_length=2, choices=Type.choices, default=Type.EXPENSE)

    is_predefined = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.type_choice} - {self.created_by}'
    


class Transaction(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH = 'CH', 'Cash'
        CARD = 'CD', 'Card'
        UPI = 'UPI', 'UPI'
        BANK_TRANSFER = 'BT', 'Bank Transfer'
        OTHER = 'OT', 'Other'
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_choice = models.CharField(max_length=2, choices=Type.choices, default=Type.EXPENSE)
    description = models.TextField(blank=True)
    payment_method = models.CharField(max_length=3, choices=PaymentMethod.choices)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True, related_name='transactions')
    transaction_date = models.DateTimeField()
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.amount} - {self.type_choice} - {self.created_by}'
    


class Budget(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='budgets')
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.category} , {self.limit}, {self.month}, {self.year} - {self.created_by}'
    

    class Meta:
        unique_together = ('created_by', 'category', 'month', 'year')

