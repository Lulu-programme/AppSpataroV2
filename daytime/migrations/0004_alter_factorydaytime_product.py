# Generated by Django 5.1.3 on 2024-12-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daytime', '0003_alter_factorydaytime_cmr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factorydaytime',
            name='product',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]