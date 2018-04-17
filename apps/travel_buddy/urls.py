from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^travels/(?P<id>\d+)$', views.show),
    url(r'^travels/(?P<id>\d+)/delete$', views.delete),
    url(r'^travels/(?P<id>\d+)/join$', views.join),
    url(r'^travels/create$', views.create),
    url(r'^new_trip$', views.new_trip)

]