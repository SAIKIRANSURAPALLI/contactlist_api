# Generated by Django 5.1.1 on 2024-09-11 18:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Contact",
        ),
    ]
