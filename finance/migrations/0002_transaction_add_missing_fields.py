from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="fee",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="transaction",
            name="logo",
            field=models.CharField(blank=True, default="", max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="transaction",
            name="name",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
