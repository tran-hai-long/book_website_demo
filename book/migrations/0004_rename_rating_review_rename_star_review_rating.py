# Generated by Django 4.1.4 on 2022-12-28 04:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("book", "0003_rating"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Rating",
            new_name="Review",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="star",
            new_name="rating",
        ),
    ]