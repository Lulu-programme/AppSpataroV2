# Generated by Django 5.1.3 on 2024-12-23 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daytime', '0004_alter_factorydaytime_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='startdaytime',
            name='last_loading',
            field=models.BooleanField(default=False),
        ),
    ]
