# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from app.forms import UploadFile
import tempfile

FILE_UPLOAD_DIR = '/tmp'

def handle_uploaded_file(file):
	fd, filepath = tempfile.mkstemp(prefix=file.name, dir=FILE_UPLOAD_DIR)
	with open(filepath, 'wb+') as dest:
		for chunk in file.chunks():
			dest.write(chunk)
	return filepath

@csrf_exempt
def upload_file(request):
	if request.method == 'POST':
		form = UploadFile(request.POST, request.FILES)
		if form.is_valid():
			filepath = handle_uploaded_file(request.FILES['file'])
			return HttpResponse(filepath)


def index(request):
	return render_to_response('home.html', context_instance = RequestContext(request))
