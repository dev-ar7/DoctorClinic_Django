from django.conf.urls import url
from . import views

app_name = 'clinic'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<appointment_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<consultation_id>[0-9]+)/isdoctor/$',
        views.isdoctor, name='isdoctor'),
    url(r'^consultation/(?P<filter_by>[a-zA-Z]+)/$',
        views.consultations, name='consultations'),
    url(r'^create_appointment/$', views.create_appoinment,
        name='create_appointment'),
    url(r'^(?P<appointment_id>[0-9]+)/create_consultation/$',
        views.create_consultation, name='create_consultation'),
    url(r'^(?P<appointment_id>[0-9]+)/delete_consultation/(?P<appointment_id>[0-9]+)/$',
        views.delete_consultation, name='delete_consultation'),
    url(r'^(?P<appointment_id>[0-9]+)/favourite_appointment/$',
        views.favourite_appointment, name='favourite_appointment'),
    url(r'^(?P<appointment_id>[0-9]+)/delete_appointment/$',
        views.delete_appointment, name='delete_appointment'),
]
