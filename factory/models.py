from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from appspataroV2.tools import zip_town


class Factory(models.Model):
    sector = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    gps = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    hourly = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    ppe = models.CharField(max_length=255, null=True, blank=True)
    tools = models.CharField(max_length=255, null=True, blank=True)
    sleep = models.BooleanField(default=False)
    reception = models.CharField(max_length=50, null=True, blank=True)
    provision = models.CharField(max_length=255, null=True, blank=True)
    plan = models.ImageField(upload_to='media', null=True, blank=True)
    description = models.TextField(blank=True)
    delete = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def get_title(self):
        return f'{self.name} - {self.city}'

    def __str__(self):
        return self.get_title()

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug},)
    
    def zip_city(self):
        return zip_town(self.country, self.zip_code, self.city)


class Station(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    delete = models.BooleanField(default=False)

    def get_title(self):
        return f'{self.name} - {self.city}'

    def __str__(self):
        return self.get_title()
    
    def zip_city(self):
        return zip_town(self.country, self.zip_code, self.city)
