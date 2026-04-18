from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.user.email or self.user.username})"


class Category(models.Model):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_CHOICES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    type = models.CharField(max_length=10, choices=Category.TYPE_CHOICES)
    date = models.DateField()
    note = models.TextField(blank=True)
    logo = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.name}: {self.amount} on {self.date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mongo_id = models.CharField(max_length=24, unique=True, editable=False)

    def __str__(self):
        return f"Profile for {self.user.email or self.user.username}"
