# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from app.forms import SubmitText
from useyourwords import settings
import tempfile
import urllib2
import json

FILE_UPLOAD_DIR = '/tmp'

def handle_uploaded_file(file):
	fd, filepath = tempfile.mkstemp(prefix=file.name, dir=FILE_UPLOAD_DIR)
	with open(filepath, 'wb+') as dest:
		for chunk in file.chunks():
			dest.write(chunk)
	return filepath

@csrf_exempt
def index(request):
	if request.method == 'POST':
		form = SubmitText(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			return HttpResponse(cd.get('textarea'))

		else:
			return render_to_response('home.html', {'form': form })
	else:
		form = SubmitText()
		return render_to_response('home.html', { 'form': form })

"""
@csrf_exempt
def index(request):
	try:
		with open(settings.WORDS_FILE, 'r') as f:
			words = json.loads(f.read())
	except IOError, e:
		print e

	return render_to_response('home.html')
"""
