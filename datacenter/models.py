from django.db import models


class Working(models.Model):
    month_year = models.DateField(auto_now=False, auto_now_add=False)
    driver_name = models.CharField(blank=True, max_length=100)
    hours_day = models.IntegerField(blank=True)
    hours_work = models.IntegerField(blank=True)
    hours_wait = models.IntegerField(blank=True)
    kms_total = models.IntegerField(blank=True)
    kms_filled = models.IntegerField(blank=True)
    kms_empty = models.IntegerField(blank=True)
    weight = models.IntegerField(blank=True)
    diesel = models.IntegerField(blank=True)
    adblue = models.IntegerField(blank=True)
    
    def get_title(self):
        return f'{self.month_year} - {self.driver_name}'
    
    def __str__(self):
        return self.get_title()


class Product(models.Model):
    month_year = models.DateField(auto_now=False, auto_now_add=False)
    un_2 = models.CharField(max_length=255, blank=True)
    weight_2 = models.IntegerField(blank=True)
    un_3 = models.CharField(max_length=255, blank=True)
    weight_3 = models.IntegerField(blank=True)
    un_4 = models.CharField(max_length=255, blank=True)
    weight_4 = models.IntegerField(blank=True)
    un_5 = models.CharField(max_length=255, blank=True)
    weight_5 = models.IntegerField(blank=True)
    un_6 = models.CharField(max_length=255, blank=True)
    weight_6 = models.IntegerField(blank=True)
    un_8 = models.CharField(max_length=255, blank=True)
    weight_8 = models.IntegerField(blank=True)
    un_9 = models.CharField(max_length=255, blank=True)
    weight_9 = models.IntegerField(blank=True)
    
    def __str__(self):
        return f'{self.month_year}'
