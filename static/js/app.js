var App = function() {
	var uploadBtn = $("#submit"),
	 	loading = $("#loading"),
	 	input = $("#file-select"),
	 	status = $("#status"),
	 	text = $("#text-input"),
	 	urlInput = $("#url-input"),
	 	submitBtn = $("#submit-text"),
	 	submitUrlBtn = $("#submit-url"),
	 	results = $("#text-results"),
	 	urlResults = $("#url-results"),
	 	elements = $("#elements"),
	 	file;

	return {
		uploadBtn: uploadBtn,
		input: input,
		submitBtn: submitBtn,
		textInput: text,
		urlInput: urlInput,
		submitUrlBtn: submitUrlBtn,

		doSubmit: function(parseUrl) {
			loading.ajaxStart(function() {
				results.hide();	
				$(this).show();
			});
			
			if (parseUrl === 'url') {
				var url = '/submit-url/';
				/*
					data = {
						url: urlInput.val(),
						elements: elements.val(),
					};
				*/
				var output = urlResults;
				var data = "url=" + urlInput.val() + "&elements=" + elements.val();

			} else {
				var url = '/submit/',
					data = text,
					output = results;
			}



			$.ajax({
				type: "POST",
				url: url,
				data: data,
				success: function(result) {
					console.log(output);
					output.html(result);
					loading.ajaxStop(function() {
						$(this).hide();
						output.show();	
					});
				}
			});
		},

		doUpload: function() {
			var formData = new FormData();

			//Just sending one file
			formData.append("file", this.files[0]);

			loading.ajaxStart(function() {
				$(this).show();
			});

			$.ajax({
				type: "POST",
				url: "/upload/",
				data: formData,
				//This will prevent jquery from making the data into a query string
				processData: false,
				contentType: false,
				statusCode: {
					500: function() {
						results.html('<div class="alert alert-error">There was a problem parsing your text.</div>');
						loading.ajaxStop(function() {
							$(this).hide();
						});
					}
				},
				success: function(result) {
					status.html("<span class='label label-success'>File uploaded </span></span>" + result + "</span>");	
					loading.ajaxStop(function() {
						$(this).hide();
					});
				}
			});
		},
	}
};

$(function() {
	var app = App();

	//See if we support ajax uploads
	if (window.FormData && window.FileReader){
		app.uploadBtn.hide();

		//app.input.bind("change", jQuery.proxy(app.doUpload, app.input));
		app.input.bind("change", app.doUpload);
	}

	app.textInput.keypress(function(event) {
		if (event.which == 13) {
			event.preventDefault();
			app.doSubmit('text');
		}
	});

	app.submitBtn.click(function(event) {
		event.preventDefault();
		app.doSubmit('text');
	});

	app.urlInput.keypress(function(event) {
		if (event.which == 13) {
			event.preventDefault();
			app.doSubmit('url');
		}
	});

	app.submitUrlBtn.click(function(event) {
		event.preventDefault();
		app.doSubmit('url');
	});
});
