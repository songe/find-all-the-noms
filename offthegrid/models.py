import datetime

from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_datetime

class Vendor(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, blank=True)
    website = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name

    def number_of_events_in_past_30_days(self):
        now = timezone.now()
        return self.events.filter(
            start_time__gte=now-datetime.timedelta(days=30),
            start_time__lte=now+datetime.timedelta(days=1)).count()

class Event(models.Model):
    id = models.CharField(max_length = 128, primary_key=True)
    name = models.CharField(max_length = 128)
    description = models.TextField(blank = True)
    start_time = models.DateTimeField(default = timezone.now)
    location = models.CharField(max_length=512, blank=True)
    vendors = models.ManyToManyField(Vendor, related_name='events')

    def __str__(self):
        return self.name

    def resolve_vendors(self):
        vendors = []
        all_vendors = Vendor.objects.values_list('id', 'name')
        for vendor_id, vendor_name in all_vendors:
            if vendor_name in self.description:
                vendor = Vendor.objects.get(id=vendor_id)
                self.vendors.add(vendor)
                vendors.append(vendor)
        return vendors

    def is_within_past_30_days(self):
        now = timezone.now()
        return (self.start_time >= now - datetime.timedelta(days=30)) and (self.stert_time <= now + datetime.timedelta(days=1))

    @classmethod
    def from_json(cls, json):
        try:
            event = cls(
                id = json['id'], # required
                name = json.get('name'),
                description = json.get('description'),
                location = json.get('location')
            )
        except KeyError:
            return None
        event.start_time = parse_datetime(json.get('start_time'))
        return event