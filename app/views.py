# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext
from app.forms import UploadFile

def index(request):
	return render_to_response('home.html', context_instance = RequestContext(request))

def upload_file(request):
	if request.method == 'POST':
		form = UploadFile(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse('success')
	else:
		form = UploadFileForm()
	return render_to_response('upload.html', {'form': form})	
