function output(msg) {
	var m = $("#status");
	m.value(msg);
}

function FileSelectHandler(e) {
	// cancel event and hover styling
	FileDragHover(e);

	//fetch filelist object
	var file = e.target.file || e.dataTransfer.file;

}

if (window.File && window.FileList && window.FileReader) {
	init();
}

function init() {
	var fileSelect = $("#file-select"),
		fileDrag = $("#file-drag"),
		submitBtn = $("#submit");
	
	fileSelect.addEventListener("change", FileSelectHandler, false);

	var xhr = new XMLHttpRequest();
	if (xhr.upload) {
		fileDrag.addEventListener("dragover", FileDragHover, false);
		fileDrag.addEventListener("dragleave", FileDragHover, false);
		fileDrag.addEventListener("drop", FileSelectHandler, false);
		fileDrag.style.display = "block";

		submitBtn.style.display = "none";
	}
}
