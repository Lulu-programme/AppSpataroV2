from django.db import models
from appspataroV2.tools import change_text_to_list


class Adr(models.Model):
    classification = models.CharField(max_length=10)
    onu = models.IntegerField(default=0)
    name = models.CharField(max_length=350)
    nsa = models.CharField(max_length=350, blank=True, null=True)
    labels = models.CharField(blank=True, max_length=20, null=True)
    packing_group = models.IntegerField(default=0, blank=True, null=True)
    tunnel_code = models.CharField(max_length=10, blank=True, null=True)
    ppe = models.TextField(blank=True, null=True)
    risks = models.TextField(blank=True, null=True)
    delete = models.BooleanField(default=False)

    def get_name(self):
        if self.nsa:
            return f'{self.onu}, {self.name}, {self.nsa}'
        return f'{self.onu}, {self.name}'
    
    def __str__(self):
        return self.get_name()

    def print_group(self):
        return '|' * self.packing_group

    def labels_change(self):
        list_labels = []
        labels = change_text_to_list(self.labels, '-')
        for label in labels:
            if '.' in label:
                change_labels = label
                change_labels = change_labels.replace('.', '_')
                list_labels.append(f'/static/images/adr/{change_labels}.jpg')
            else:
                if label.lower() == 'environnement':
                    list_labels.append('/static/images/adr/env.png')
                elif label.lower() == 'température':
                    list_labels.append('/static/images/adr/temp.jpg')
                else:
                    list_labels.append(f'/static/images/adr/{label}.jpg')
        return list_labels

    def labels_list(self):
        labels_list = []
        labels = change_text_to_list(self.labels, '-')
        for label in labels:
            if not label.lower() == 'environnement' and not label.lower() == 'température':
                labels_list.append(label)
        return ', '.join(labels_list)
