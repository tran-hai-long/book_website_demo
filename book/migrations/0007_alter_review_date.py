# Generated by Django 4.1.4 on 2022-12-28 07:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0006_review_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
