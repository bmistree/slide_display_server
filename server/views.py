from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import models
from django.core.urlresolvers import reverse
import datetime

def index(request):
    '''
    Display original page.  If have a get parameter, starts displaying
    resources from that point forward.
    '''
    if request.method == 'GET':
        from_param = request.GET.get('from',1)
        return render_to_response(
            'main.html',
            {'from': from_param},
            context_instance=RequestContext(request))

    return HttpResponseNotFound('<h1>Incorrect http method</h1>')

def check_reserved(request):
    '''
    The site polls every hour to see if it should change to a reserved
    image.  This just checks if
    '''
    now = datetime.datetime.now()
    reserved_list = models.Reservation.objects.filter(
        start__lte=now).filter(end__gte=now)
    update_val_pk = 0    
    if len(reserved_list) != 0:
        reservation = reserved_list[0]
        update_val_pk = reservation.resource.id
        
    return HttpResponse(str(update_val_pk),mimetype='text/html')


def next_url(request):
    '''
    Approximately every 24 hours, the site requests a new random poster
    to display.  This makes that request.
    '''
    if request.method == 'GET':
        from_param = int(request.GET.get('from',1))
        last_resource = models.WebResource.objects.latest('creation_date')
        num_resources = last_resource.pk
        if num_resources == 0:
            return HttpResponseNotFound('<h1>You must load resources for this to work</h1>')            
        
        resource_to_select = from_param % (num_resources + 1)
        while True:
            try:
                to_display = models.WebResource.objects.get(pk=int(resource_to_select))
                break
            except:
                resource_to_select += 1
                pass

        res_file_pk = to_display.id
        return HttpResponse(str(res_file_pk),mimetype='text/html')

def resource_url(request):
    '''
    Returns the resource requested by the key requested
    '''
    if request.method == 'GET':
        resource_pk = int(request.GET.get('resource_pk',0))
        if resource_pk != 0:
            try:
                resource = models.WebResource.objects.get(pk = resource_pk)
                resource_data = resource.resource_file

                if resource.resource_type == models.WebResource.JPG_TYPE:
                    return HttpResponse(resource_data,mimetype='image/jpeg')
                elif resource.resource_type == models.WebResource.PNG_TYPE:
                    return HttpResponse(resource_data,mimetype='image/png')
                elif resource.resource_type == models.WebResource.HTML_TYPE:
                    return HttpResponse(resource_data,mimetype='text/html')
                
            except:
                pass


    return HttpResponseNotFound('<h1>Requested unknown resource</h1>')
    
