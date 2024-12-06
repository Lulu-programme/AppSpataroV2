from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Factory(models.Model):
    sector = models.CharField(max_length=255)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    gps = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    hourly = models.CharField(max_length=50)
    language = models.CharField(max_length=255)
    ppe = models.CharField(max_length=255)
    tools = models.CharField(max_length=255)
    sleep = models.BooleanField(default=False)
    reception = models.CharField(max_length=50)
    provision = models.CharField(max_length=255)
    plan = models.ImageField(upload_to='media')
    description = models.TextField(blank=True)
    delete = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return f'{self.name} - {self.city}'

    def name_city(self):
        return f'{self.name} - {self.city}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}-{self.town}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug},)
    
    
class Station(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.city}'
    
