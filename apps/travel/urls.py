from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new$', new, name='new'),
    url(r'^create$', create, name='create'),
    url(r'^join/(?P<trip_id>\d+)$', join, name='join'),
    url(r'^cancel/(?P<trip_id>\d+)$', cancel, name='cancel'),
    url(r'^show/(?P<trip_id>\d+)$', show, name='show'),
    url(r'^delete/(?P<trip_id>\d+)$', delete, name='delete'),
]
