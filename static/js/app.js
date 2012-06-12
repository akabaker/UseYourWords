var App = function() {
	var uploadBtn = $("#submit"),
	 	loading = $("#loading"),
	 	input = $("#file-select"),
	 	status = $("#status"),
	 	text = $("#text-input"),
	 	url = $("#url-input"),
	 	submitBtn = $("#submit-text"),
	 	results = $("#results"),
	 	file;

	return {
		uploadBtn: uploadBtn,
		input: input,
		submitBtn: submitBtn,

		doSubmit: function() {
			loading.ajaxStart(function() {
				results.hide();	
				$(this).show();
			});

			$.ajax({
				type: "POST",
				url: "/submit/",
				data: $.param(text),
				success: function(result) {
					$("#results").html(result);
					//window.history.pushState(result, "results", "#results");
					loading.ajaxStop(function() {
						$(this).hide();
						results.show();	
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
						$("#results").html('<div class="alert alert-error">There was a problem parsing your text.</div>');
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

	app.submitBtn.click(function(event) {
		event.preventDefault();
		app.doSubmit();
	});
});
