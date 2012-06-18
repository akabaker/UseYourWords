# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from app.forms import SubmitText, SubmitUrl
from useyourwords import settings
from BeautifulSoup import BeautifulSoup as bs
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

def parse_url(url, elements):
	html = urllib2.urlopen(urllib2.Request(url)).read()
	soup = bs(html)
	words = []

	for elem in elements:
		for line in soup.findAll(elem): words.append(line.text)
	
	return ' '.join(words)
	#freq = nltk.FreqDist(nltk.word_tokenize(' '.join(words)))

@csrf_exempt
def submit_url(request):
	if request.is_ajax:
		if request.method == 'POST':
			form = SubmitUrl(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				parsed_text = parse_url(cd.get('url'), cd.get('elements'))
				freq = calc_word_freq(parsed_text)
				word_count = freq.N()
				cloud = generate_word_cloud(freq)
				results = {'freq': freq.items(), 'cloud': cloud, 'word_count': word_count }
				return render_to_response('results.html', { 'results': results })	
			else:
				return HttpResponse('<div class="alert alert-error">%s</div>' % form.errors)

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
			return HttpResponse('<div class="alert alert-error">%s</div>' % form.errors)

@csrf_exempt
def index(request):
	try:
		with open(settings.WORDS_FILE, 'r') as f:
			words = json.loads(f.read())
	except IOError, e:
		print e

	return render_to_response('home.html')
