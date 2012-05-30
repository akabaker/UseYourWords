# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from app.forms import UploadFile
import tempfile

def handle_uploaded_file(file):
	#temp = tempfile.NamedTemporaryFile()
	#for chunk in file.chunks():
	#	temp.write(chunk)
	with open('/tmp/tmpfile', 'wr+') as f:
		for chunk in file.chunks():
			f.write(chunk)

def index(request):
	return render_to_response('home.html', context_instance = RequestContext(request))

@csrf_exempt
def upload_file(request):
	errors = []
	if request.method == 'POST':
		form = UploadFile(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse('success')

		else:
			return render_to_response('home.html')	
	else:
		form = UploadFileForm()
	return render_to_response('home.html')	
