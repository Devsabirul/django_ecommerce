# Generated by Django 4.1.6 on 2023-04-28 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_seller",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
