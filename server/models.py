from django.db import models
from django.contrib import admin

from registration.signals import user_activated
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms

def login_on_activation(sender, user, request, **kwargs):
    '''
    Logs in the user after activation
    '''
    
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
 
# Registers the function with the django-registration user_activated
# signal
user_activated.connect(login_on_activation)


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        app_label = 'server'

def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 


class WebResource(models.Model):
    resource_name = models.TextField()
    resource_creater = models.ForeignKey(User)
    expiration_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now = True)
    description = models.TextField()
    allow_random = models.BooleanField()
    resource_file = models.FileField(upload_to='uploaded')

    JPG_TYPE = 'JPG'
    PNG_TYPE = 'PNG'
    HTML_TYPE = 'HTML'
    RESOURCE_TYPES = (
        (JPG_TYPE, 'jpeg'),
        (PNG_TYPE,'png'),
        (HTML_TYPE,'html'))
    resource_type = models.CharField(
        max_length=4,
        choices=RESOURCE_TYPES)

    class Meta:
        app_label = 'server'

    def __unicode__ (self):
        return self.resource_name
    
    def __str__ (self):
        return self.resource_name


def validate_no_time_overlap(value):
    interfering = Reservation.objects.filter(
        start__lte=value).filter(end__gte=value)
    if len(interfering) != 0:
        err_msg = 'Time specified interferes with an existing reservation: '
        err_msg += str(interfering[0].resource)
        raise forms.ValidationError(err_msg)
    
class Reservation(models.Model):
    resource = models.ForeignKey(WebResource)
    owner = models.ForeignKey(User)
    start = models.DateTimeField(validators=[validate_no_time_overlap])
    end = models.DateTimeField(validators=[validate_no_time_overlap])

    class Meta:
        app_label = 'server'

    def __str__(self):
        return str(self.resource)
    def __unicode__(self):
        return unicode(self.resource)

