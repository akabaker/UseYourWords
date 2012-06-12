# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from app.forms import SubmitText, SubmitUrl
from useyourwords import settings
from BeautifulSoup import BeautifulSoup
import math
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
	result = {}

	for word, word_count in words.items():
		font_size = word_count * 8
		if font_size >= 150:
			result[word] = 150
		else:
			result[word] = str(font_size)
	return result

def parse_url(url):
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	paragraphs = soup.findAll('p')

	text = []
	for p in paragraphs:
		text.append(p.text)

	return HttpResponse(text)

@csrf_exempt
def submit_text(request):
	if request.method == 'POST':
		form = SubmitText(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			freq = calc_word_freq(cd.get('textarea'))
			word_count = freq.N()
			cloud = generate_word_cloud(freq)
			results = {'freq': freq.items(), 'cloud': cloud, 'word_count': word_count }
			return render_to_response('results.html', { 'results': results })	

		else:
			#return render_to_response('home.html', {'form': form })
			return HttpResponse('<div class="alert alert-error">Please insert some text</div>')
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
