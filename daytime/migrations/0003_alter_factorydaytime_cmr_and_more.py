# Generated by Django 5.1.3 on 2024-12-21 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daytime', '0002_alter_factorydaytime_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factorydaytime',
            name='cmr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='command',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='product',
            field=models.TextField(blank=True, null=True),
        ),
    ]