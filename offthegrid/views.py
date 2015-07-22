from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from .models import Vendor, Event

import requests
import os

def index(request):
    return event_list(request)

def event_list(request):
    event_list = load_event_list_from_facebook(2) or Event.objects.all()
    template = loader.get_template('offthegrid/events.html')
    context = RequestContext(request, { 'event_list': event_list })
    return HttpResponse(template.render(context))

def event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        event = load_event_from_facebook(event_id)

    template = loader.get_template('offthegrid/event.html')
    context = RequestContext(request, { 'event': event })
    return HttpResponse(template.render(context))

def vendor_list(request):
    vendors = list(Vendor.objects.all())
    vendors.sort(key = lambda v: (v.number_of_events_in_past_30_days(), v.events.count()), reverse=True)
    template = loader.get_template('offthegrid/vendors.html')
    context = RequestContext(request, { 'vendors': vendors })
    return HttpResponse(template.render(context))

def vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except ObjectDoesNotExist:
        vendor = None
    template = loader.get_template('offthegrid/vendor.html')
    context = RequestContext(request, { 'vendor': vendor })
    return HttpResponse(template.render(context))

### FIXME: clean it up
GRAPH_API = 'https://graph.facebook.com/'
OFF_THE_GRID = GRAPH_API + 'OffTheGridSF/events'
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
AUTH = {'access_token': ACCESS_TOKEN}

def load_event_list_from_facebook(pages=2):
    events = []

    url = OFF_THE_GRID
    for i in range(pages):
        r = requests.get(url, params=AUTH)
        try:
            events.extend(r.json().get('data'))
        except Exception:
            # ACCESS_TOKEN is probably expired; just return empty events
            return events
        url = r.json().get('paging').get('next')

    for event in events:
        event_id = event.get('id')
        if not Event.objects.filter(id=event_id).exists():
            load_event_from_facebook(event_id)

    return events

def load_event_from_facebook(event_id):
    r = requests.get(GRAPH_API + event_id, params=AUTH)
    event = Event.from_json(r.json())
    event.save()
    event.resolve_vendors()
    return event
