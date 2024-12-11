from django.db import models


class Working(models.Model):
    month_year = models.CharField(max_length=100, blank=True)
    driver_name = models.CharField(blank=True, max_length=100)
    hours_day = models.IntegerField(blank=True)
    hours_work = models.IntegerField(blank=True)
    hours_wait = models.IntegerField(blank=True)
    kms_total = models.IntegerField(blank=True)
    kms_filled = models.IntegerField(blank=True)
    kms_empty = models.IntegerField(blank=True)
    wheight = models.IntegerField(blank=True)
    diesel = models.IntegerField(blank=True)
    adblue = models.IntegerField(blank=True)
    
    def get_title(self):
        return f'{self.month_year} - {self.driver_name}'
    
    def __str__(self):
        return self.get_title()


class Product(models.Model):
    month_year = models.CharField(max_length=100, blank=True)
    un_2 = models.CharField(max_length=255, blank=True)
    wheight_2 = models.CharField(max_length=255, blank=True)
    un_3 = models.CharField(max_length=255, blank=True)
    wheight_3 = models.CharField(max_length=255, blank=True)
    un_4 = models.CharField(max_length=255, blank=True)
    wheight_4 = models.CharField(max_length=255, blank=True)
    un_5 = models.CharField(max_length=255, blank=True)
    wheight_5 = models.CharField(max_length=255, blank=True)
    un_6 = models.CharField(max_length=255, blank=True)
    wheight_6 = models.CharField(max_length=255, blank=True)
    un_8 = models.CharField(max_length=255, blank=True)
    wheight_8 = models.CharField(max_length=255, blank=True)
    un_9 = models.CharField(max_length=255, blank=True)
    wheight_9 = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.month_year
