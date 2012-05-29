# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext

def index(request):
	return render_to_response('base.html', context_instance = RequestContext(request))
