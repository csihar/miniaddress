from django.shortcuts import render_to_response
from django.template import RequestContext
from miniaddress.models import House, Owner

def home(request):
	houses = House.objects.all().order_by('id')
	owners = Owner.objects.all().order_by('id')
	return render_to_response('index.html', {'houses': houses, 'owners': owners}, RequestContext(request))
