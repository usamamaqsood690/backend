from django.contrib import admin
from .models import Account, Category, Transaction, UserProfile


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "balance")
    search_fields = ("name", "user__email", "user__username")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "user")
    list_filter = ("type",)
    search_fields = ("name", "user__email", "user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "account", "category", "amount", "fee", "type", "date")
    list_filter = ("type", "date")
    search_fields = ("name", "note", "user__email", "user__username")
    autocomplete_fields = ("user", "account", "category")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "mongo_id")
    search_fields = ("user__email", "user__username", "mongo_id")
