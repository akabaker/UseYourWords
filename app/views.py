# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from app.forms import SubmitText
from useyourwords import settings
import nltk
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

def calc_word_freq(words):
	freq = nltk.FreqDist(nltk.word_tokenize(words))
	return freq
	
def generate_word_cloud(words):
	#CSS font sizes
	font_sizes = [10,20,30,40]
	max_num = max(words.values())

	#Interval
	step = max_num / len(range(0,2))

	result = {}
	for word, count in words.items():
		font_size_index = count / step
		#result += '<span style="font-size:%dpx">%s - %d</span>' % (font_sizes[font_size_index], word, count)
		result[word] = font_sizes[font_size_index]

	return result

@csrf_exempt
def submit_text(request):
	if request.method == 'POST':
		form = SubmitText(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			freq = calc_word_freq(cd.get('textarea'))
			cloud = generate_word_cloud(freq)
			results = {'freq': freq.items(), 'cloud': cloud }
			return render_to_response('results.html', { 'results': results })	

		else:
			#return render_to_response('home.html', {'form': form })
			return HttpResponse('errors')

	#else:
	#	form = SubmitText()
	#	return render_to_response('home.html', { 'form': form })

@csrf_exempt
def index(request):
	try:
		with open(settings.WORDS_FILE, 'r') as f:
			words = json.loads(f.read())
	except IOError, e:
		print e

	return render_to_response('home.html')
