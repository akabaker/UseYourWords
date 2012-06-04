var App = function() {
	var uploadBtn = $("#submit");
	var status = $("#status");
	var input = $("#file-select");

	return {
		uploadBtn: uploadBtn,
		input: input,
		doUpload: function(event) {

				$.ajax({
					type: "POST",
					url: "/upload/",
					data: data,
					//This will prevent jquery from making the data into a query string
					processData: false,
					contentType: false,
					statusCode: {
						500: function() {
							console.log("http500");
						}
					},
					success: function(result) {
						console.log(result);
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

		app.input.bind("change", event, app.doUpload);
	}
});
