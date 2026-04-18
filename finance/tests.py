from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Account, Category, Transaction


class AuthApiTests(APITestCase):
    def test_register_creates_user_and_returns_tokens(self):
        response = self.client.post(
            reverse("register"),
            {"email": "owner@example.com", "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["email"], "owner@example.com")
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])
        self.assertNotIn("username", response.data["data"])
        self.assertTrue(User.objects.filter(email="owner@example.com").exists())

    def test_login_with_email_returns_tokens(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass123",
        )

        response = self.client.post(
            reverse("email_login"),
            {"email": user.email, "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["email"], user.email)
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])


class TransactionApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass123",
        )
        self.other_user = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="StrongPass123",
        )
        self.account = Account.objects.create(user=self.user, name="Checking", balance="1000.00")
        self.category = Category.objects.create(user=self.user, name="Salary", type="income")
        self.other_account = Account.objects.create(user=self.other_user, name="Hidden", balance="500.00")
        self.client.force_authenticate(user=self.user)

    def test_create_transaction_assigns_authenticated_user(self):
        response = self.client.post(
            reverse("transaction-create"),
            {
                "account": self.account.id,
                "category": self.category.id,
                "name": "April Salary",
                "amount": "2500.00",
                "fee": "0.00",
                "type": "income",
                "date": "2026-04-18",
                "logo": "",
                "note": "Monthly salary",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(name="April Salary")
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.account, self.account)

    def test_create_transaction_rejects_other_users_account(self):
        response = self.client.post(
            reverse("transaction-create"),
            {
                "account": self.other_account.id,
                "category": self.category.id,
                "name": "Invalid",
                "amount": "50.00",
                "fee": "0.00",
                "type": "income",
                "date": "2026-04-18",
                "logo": "",
                "note": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("account", response.data)

    def test_list_transactions_is_paginated_filtered_and_user_scoped(self):
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            name="Latest Salary",
            amount="2600.00",
            fee="0.00",
            type="income",
            date="2026-04-18",
            note="",
            logo="",
        )
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            name="Older Salary",
            amount="2400.00",
            fee="0.00",
            type="income",
            date="2026-04-01",
            note="",
            logo="",
        )
        Transaction.objects.create(
            user=self.other_user,
            account=self.other_account,
            category=None,
            name="Other User Transaction",
            amount="500.00",
            fee="0.00",
            type="income",
            date="2026-04-18",
            note="",
            logo="",
        )

        response = self.client.get(
            reverse("transaction-list"),
            {"type": "income", "start_date": "2026-04-10"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Latest Salary")
        self.assertEqual(response.data["results"][0]["typeoftrans"], "income")
