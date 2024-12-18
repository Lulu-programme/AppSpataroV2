# Generated by Django 5.1.3 on 2024-12-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daytime', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changedaytime',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='changedaytime',
            name='condition',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='changedaytime',
            name='hour_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='changedaytime',
            name='lights',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='changedaytime',
            name='tires',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='changedaytime',
            name='trailer',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='cmr',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='command',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='end_work',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='hour_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='km_empty',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='km_filled',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='product',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='start_work',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='factorydaytime',
            name='wheight',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gasoildaytime',
            name='adblue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gasoildaytime',
            name='diesel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gasoildaytime',
            name='hour_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startdaytime',
            name='city_end',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='startdaytime',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startdaytime',
            name='hour_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startdaytime',
            name='km_end',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
