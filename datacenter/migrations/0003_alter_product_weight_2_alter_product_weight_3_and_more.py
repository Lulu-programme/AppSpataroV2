# Generated by Django 5.1.3 on 2025-01-12 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0002_rename_wheight_2_product_weight_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_2',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_3',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_4',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_5',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_6',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_8',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_9',
            field=models.IntegerField(blank=True),
        ),
    ]