from django.db import models
from appspataroV2.tools import calculate_laps_time, hours_seconds, convert_seconds


class StartDaytime(models.Model):
    name_driver = models.CharField(max_length=100)
    truck = models.CharField(max_length=100)
    trailer = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    city_start = models.CharField(max_length=100)
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False)
    km_start = models.IntegerField()
    city_end = models.CharField(max_length=100, blank=True)
    date_end = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    hour_end = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    km_end = models.IntegerField(blank=True, null=True)
    work = models.JSONField(default=list)
    compled = models.BooleanField(default=False)
    formel = models.CharField(default='start', max_length=50)

    def __str__(self):
        return f'{self.name_driver}'

    def total_km(self):
        return self.km_end - self.km_start

    def hours_to_string(self, start):
        if start:
            return f'{self.hour_start.hour:02}h{self.hour_start.minute:02}'
        return f'{self.hour_end.hour:02}h{self.hour_end.minute:02}'

    def total_hours(self):
        if self.date_start == self.date_end:
            return calculate_laps_time(self.hour_start.hour, self.hour_end.hour, self.hour_start.minute, self.hour_end.minute, True)
        else:
            hours_1 = calculate_laps_time(self.hour_start.hour, 24, self.hour_start.minute, 0, False)
            hours_2 = calculate_laps_time(0, self.hour_end.hour, 0, self.hour_end.minute, False)
            return convert_seconds(hours_1 + hours_2, True)
    
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
        self.trailer = f'{self.trailer} - {new_trailer}'
        self.save()


class FactoryDaytime(models.Model):
    name = models.CharField(max_length=100)
    hour_arrival = models.TimeField(auto_now=False, auto_now_add=False)
    km_arrival = models.IntegerField()
    start_work = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    end_work = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    cmr = models.TextField(blank=True)
    command = models.TextField(blank=True)
    product = models.CharField(max_length=100, blank=True, null=True)
    wheight = models.IntegerField(blank=True, null=True)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    comment = models.TextField(blank=True)
    km_filled = models.IntegerField(blank=True, null=True)
    km_empty = models.IntegerField(blank=True, null=True)
    compled = models.BooleanField(default=False)
    formel = models.CharField(default='factory', max_length=50)

    def __str__(self):
        return self.name

    def total_work(self):
        return calculate_laps_time(self.start_work.hour, self.end_work.hour, self.start_work.minute, self.end_work.minute, True)
    
    def total_wait(self):
        to_place = calculate_laps_time(self.hour_arrival.hour, self.hour_start.hour, self.hour_arrival.minute, self.hour_start.minute, False)
        to_work = calculate_laps_time(self.start_work.hour, self.end_work.hour, self.start_work.minute, self.end_work.minute, False)
        return convert_seconds(to_place - to_work, True)


class ChangeDaytime(models.Model):
    name = models.CharField(max_length=100)
    hour_arrival = models.TimeField(auto_now=False, auto_now_add=False)
    km_arrival = models.IntegerField()
    trailer = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=100, blank=True)
    lights = models.CharField(max_length=100, blank=True)
    tires = models.CharField(max_length=100, blank=True)
    wheight = models.BooleanField(default=False)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    comment = models.TextField(blank=True)
    compled = models.BooleanField(default=False)
    formel = models.CharField(default='change', max_length=50)

    def __str__(self):
        return self.name


class GasoilDaytime(models.Model):
    name = models.CharField(max_length=100)
    hour_arrival = models.TimeField(auto_now=False, auto_now_add=False)
    km_arrival = models.IntegerField()
    diesel = models.IntegerField(blank=True, null=True)
    adblue = models.IntegerField(blank=True, null=True)
    hour_start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    compled = models.BooleanField(default=False)
    formel = models.CharField(default='gasoil', max_length=50)

    def __str__(self):
        return self.name
