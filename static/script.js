const preview = document.getElementById("preview");
const startBtn = document.getElementById("startBtn");
const timer = document.getElementById("timer");
const status = document.getElementById("status");

let stream = null;
let recorder = null;
let chunks = [];


// =========================
// CAMERA START
// =========================

async function startCamera() {

    try {

        stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });

        preview.srcObject = stream;

        status.innerText = "✅ Camera ready";

    } catch (error) {

        console.error(error);

        status.innerText =
            "❌ Camera permission allow karein";

    }
}


// =========================
// RECORDING
// =========================

startBtn.addEventListener("click", async function () {

    if (!stream) {

        await startCamera();

    }

    if (!stream) {

        return;

    }


    chunks = [];


    recorder = new MediaRecorder(stream);


    recorder.ondataavailable = function(event) {

        if (event.data.size > 0) {

            chunks.push(event.data);

        }

    };


    recorder.onstop = function() {

        uploadVideo();

    };


    recorder.start();


    startBtn.disabled = true;

    status.innerText = "🔴 Recording...";


    let time = 5;

    timer.innerText = time + " seconds";


    const countdown = setInterval(function () {

        time--;

        if (time > 0) {

            timer.innerText = time + " seconds";

        } else {

            clearInterval(countdown);

            timer.innerText = "Uploading...";

            recorder.stop();

        }

    }, 1000);

});


// =========================
// UPLOAD
// =========================

async function uploadVideo() {

    const blob = new Blob(
        chunks,
        {
            type: "video/webm"
        }
    );


    const formData = new FormData();


    formData.append(
        "video",
        blob,
        "recording.webm"
    );


    try {

        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );


        const result = await response.json();


        if (result.success) {

            status.innerText =
                "✅ Video successfully save ho gayi!";

            timer.innerText = "Completed";

        } else {

            status.innerText =
                "❌ Video upload nahi hui.";

        }

    } catch (error) {

        console.error(error);

        status.innerText =
            "❌ Server connection error.";

    }


    startBtn.disabled = false;

}


// Camera start
startCamera();