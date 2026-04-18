from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_transaction_add_missing_fields"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="transaction",
            options={"ordering": ["-date", "-id"]},
        ),
        migrations.AlterField(
            model_name="category",
            name="type",
            field=models.CharField(
                choices=[("income", "Income"), ("expense", "Expense")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="type",
            field=models.CharField(
                choices=[("income", "Income"), ("expense", "Expense")],
                max_length=10,
            ),
        ),
    ]
