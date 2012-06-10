from django import forms

class UploadFile(forms.Form):
	file = forms.FileField()

class SubmitText(forms.Form):
	textarea = forms.CharField(max_length=5000, min_length=2)

	"""
	def clean_message(self):
		data = self.cleaned_data['textarea']
		if (len(data) == 0):
			raise forms.ValidationError('Please provide some text')
		return data
	"""
