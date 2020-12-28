# Generated by Django 3.1.4 on 2020-12-27 09:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("savings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="performed_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]