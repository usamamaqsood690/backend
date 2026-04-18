# Transaction APIs ✅ Updated with create + new fields
**Run**: python manage.py makemigrations && python manage.py migrate


## Test Instructions:
1. Run `python manage.py runserver`
2. Register: POST `/api/register/` {"email": "test@example.com", "password": "pass123"}
3. Login: POST `/api/login/` → get access token
4. Create sample transaction via Django admin (`python manage.py createsuperuser` first, then /admin/)
5. GET `/api/finance/transactions/` with `Authorization: Bearer <access_token>`

**Fields**: transid(id), name(category.name), amount, fee(0), datetime(date), typeoftrans(type), logo('')
