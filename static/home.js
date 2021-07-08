const uploadForm = document.getElementById("upload-form");
const input = document.getElementById("uploadVideoFile");
const alertBox = document.getElementById("alert-box");
const videoBox = document.getElementById("video-box");
const progressBox = document.getElementById("progress-box");
const cancelBox = document.getElementById("cancel-box");
const cancelBtn = document.getElementById("cancel-btn");
const csrf = document.getElementsByName('csrfmiddlewaretoken');
const nodeAppUrl = 'http://13.233.84.46:8080';

input.addEventListener("change", function(){
    progressBox.classList.remove('not-visible');
    cancelBox.classList.remove('not-visible');

    const video_data = input.files[0];
    const url = URL.createObjectURL(video_data);
    console.log(video_data);

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('video', video_data)



    $.ajax({
        type: 'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){
            console.log('before');
            alertBox.innerHTML = '';


        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', function(e){
                // console.log(e);
                if(e.lengthComputable){
                    const percent = e.loaded / e.total * 100;
                    console.log(percent);
                    progressBox.innerHTML = `<div class="progress">
                                            <div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <p>${percent.toFixed(1)}% </p>`
                }
            })

            cancelBtn.addEventListener("click", function(){
                xhr.abort();
                progressBox.innerHTML="";
                cancelBox.classList.add('not-visible');
            })

            return xhr;
        },
        success: function(response){
            progressBox.innerHTML = "";
            uploadForm.reset();
            console.log(response);
            videoBox.innerHTML = `<video id="video" src="${url}"  style="width: 100%;" controls muted>
            </video>
            <a class="btn btn-outline-info mt-2 mb-2" href="${nodeAppUrl}/${response.roomid}/${response.file_name}/">Sync Video</a>`

            alertBox.innerHTML = `<div class="alert alert-success" role="alert">
            Successfully uploaded the video</div>`
            cancelBox.classList.add('not-visible');
        },
        error: function(error){
            console.log(error);
        },
        cache: false,
        contentType: false,
        processData: false
    });
})


function input_filename() {

    file_input_label.innerText = input.files[0].name;

}
