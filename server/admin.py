from django.contrib import admin
from models import WebResource, Reservation

class WebResourceAdmin(admin.ModelAdmin):
    fields = [
        'resource_name','resource_creater','expiration_date',
        'description','allow_random','resource_file','resource_type']
    list_display = ['resource_name', 'resource_creater']
    ordering = ['resource_name']

class ReservationAdmin(admin.ModelAdmin):
    fields = [
        'resource','owner','start','end' ]
    list_display = [ 'resource','owner','start','end' ]
    ordering = ['start']

admin.site.register(WebResource,WebResourceAdmin)
admin.site.register(Reservation,ReservationAdmin)



# get rid of junk that do not care about.
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
admin.site.unregister(Group)
admin.site.unregister(Site)

