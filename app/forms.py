from django import forms

class UploadFile(forms.Form):
	file = forms.FileField()

class SubmitText(forms.Form):
	#textarea = forms.CharField(max_length=5000, min_length=2)
	textarea = forms.CharField(min_length=2)

CHOICES = (
	('p', 'p'),
	('h1', 'h1'),
)

class SubmitUrl(forms.Form):
	url = forms.CharField(min_length=7)
	elements = forms.MultipleChoiceField(choices=CHOICES)
