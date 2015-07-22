from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    # ex: /off-the-grid/
    url(r'^$', RedirectView.as_view(url='events', permanent=False)),

    # ex: /off-the-grid/events/
    url(r'^events/$', views.event_list, name='event_list'),

    # ex: /off-the-grid/event/12345/
    url(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),

    # ex: /off-the-grid/vendors/
    url(r'^vendors/$', views.vendor_list, name='vendor_list'),

    # ex: /off-the-grid/vendor/the-vendor-name/
    url(r'^vendor/(?P<vendor_id>[\w-]+)/$', views.vendor, name='vendor'),
]