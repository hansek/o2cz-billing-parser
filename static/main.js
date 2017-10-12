o2_drop = Dropzone.options.myAwesomeDropzone = {
    paramName: "file", // The name that will be used to transfer the file
    maxFiles: 1,
    maxFilesize: 2, // MB
    createImageThumbnails: false,
    acceptedFiles: '.zip',
    dictDefaultMessage: 'Šup sem s tím ZIPem',

    init: function() {
        this.on('complete', function(file) {
            this.removeFile(file);

            document.getElementById('result').innerHTML = '';

            if (file.xhr.status == 200) {
                document.getElementById('result').innerHTML = file.xhr.response
            } else {
                // DEBUG use
                // document.body.innerHTML = file.xhr.response
                alert(file.xhr.responseText);
            }

        });
    }
};
