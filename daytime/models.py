from django.db import models
from appspataroV2.tools import calculate_laps_time, convert_seconds


class StartDaytime(models.Model):
    driver_name = models.CharField(max_length=100)
    truck = models.CharField(max_length=100)
    trailer = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100)
    city_start = models.CharField(max_length=100)
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False)
    km_start = models.IntegerField()
    city_end = models.CharField(max_length=100, blank=True)
    date_end = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    hour_end = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    km_end = models.IntegerField(blank=True, null=True)
    work = models.JSONField(default=list, blank=True, null=True)
    last_load = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    formal = models.CharField(default='start', max_length=50)

    def __str__(self):
        return f'{self.driver_name} - {self.truck} - {self.date_start}'

    def total_km(self):
        return self.km_end - self.km_start

    def hours_to_string(self, start):
        if start:
            return f'{self.hour_start.hour:02}h{self.hour_start.minute:02}'
        return f'{self.hour_end.hour:02}h{self.hour_end.minute:02}'

    def total_hours(self, string):
        return calculate_laps_time(self.hour_start.hour, self.hour_end.hour, self.hour_start.minute, self.hour_end.minute, string)
    
    def add_work(self, work_id, work_type):
        """
        Ajoute un travail dans le champ JSONField `work`.
        """
        self.work.append({"id": work_id, "type": work_type})
        self.save()

    def get_work_by_type(self, work_type):
        """
        Récupère les IDs des travaux d'un type spécifique.
        """
        return [work["id"] for work in self.work if work["type"] == work_type]
    
    def get_work(self):
        return [work for work in self.work]
    
    def add_trailer(self, new_trailer):
        if self.trailer[-1] == '.':
            self.trailer = f'{self.trailer[:-1].strip()}, {new_trailer}.'
        else:
            self.trailer = f'{self.trailer}, {new_trailer}.'
        self.save()
        
    def set_last_load(self, load):
        self.last_load = load


class FactoryDaytime(models.Model):
    name = models.CharField(max_length=100)
    arrival_hour = models.TimeField(auto_now=False, auto_now_add=False)
    km_arrival = models.IntegerField()
    work_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    end_work = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    cmr = models.TextField(blank=True, null=True)
    command = models.TextField(blank=True, null=True)
    product = models.JSONField(default=list, blank=True, null=True)
    weight = models.IntegerField(default=0)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    km_filled = models.IntegerField(blank=True, null=True)
    km_emptied = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    formal = models.CharField(default='factory', max_length=50)

    def __str__(self):
        return self.name

    def total_work(self, string):
        return calculate_laps_time(self.work_start.hour, self.end_work.hour, self.work_start.minute, self.end_work.minute, string)
    
    def total_wait(self, string):
        to_place = calculate_laps_time(self.arrival_hour.hour, self.hour_start.hour, self.arrival_hour.minute, self.hour_start.minute, False)
        to_work = calculate_laps_time(self.work_start.hour, self.end_work.hour, self.work_start.minute, self.end_work.minute, False)
        return convert_seconds(to_place - to_work, string)
    
    def add_product(self, product_id, product_type, product_class):
        """
        Ajoute un produit dans le champ JSONField `product`.
        """
        self.product.append({"id": product_id, "name": product_type, "classification": product_class})
        self.save()
    
    def get_product(self):
        return [product for product in self.product]


class ChangeDaytime(models.Model):
    name = models.CharField(max_length=100)
    arrival_hour = models.TimeField(auto_now=False, auto_now_add=False)
    km_arrival = models.IntegerField()
    trailer = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=100, blank=True)
    lights = models.CharField(max_length=100, blank=True)
    tires = models.CharField(max_length=100, blank=True)
    weight = models.IntegerField(default=0)
    cmr = models.TextField(blank=True, null=True)
    command = models.TextField(blank=True, null=True)
    product = models.JSONField(default=list, blank=True, null=True)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    comment = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    formal = models.CharField(default='change', max_length=50)

    def __str__(self):
        return self.name
    
    def add_product(self, product_id, product_type, product_class):
        """
        Ajoute un produit dans le champ JSONField `product`.
        """
        self.product.append({"id": product_id, "name": product_type, "classification": product_class})
        self.save()


class GasoilDaytime(models.Model):
    name = models.CharField(max_length=100)
    arrival_hour = models.TimeField(auto_now=False, auto_now_add=False)
    km_arrival = models.IntegerField()
    diesel = models.IntegerField(blank=True, null=True)
    adblue = models.IntegerField(blank=True, null=True)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    completed = models.BooleanField(default=False)
    formal = models.CharField(default='gasoil', max_length=50)

    def __str__(self):
        return self.name
