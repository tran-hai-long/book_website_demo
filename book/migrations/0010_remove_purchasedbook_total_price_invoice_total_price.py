# Generated by Django 4.1.4 on 2022-12-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0009_invoice_purchasedbook"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchasedbook",
            name="total_price",
        ),
        migrations.AddField(
            model_name="invoice",
            name="total_price",
            field=models.FloatField(default=0),
        ),
    ]
