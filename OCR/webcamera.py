class WebcamCaptureHTML:
    def __init__(self):
        self.html_code = """
            <div style="display: flex; justify-content: center;">
                <video id="webcam" width="640" height="480" autoplay></video>
                <button id="capture" style="margin-top: 10px;">Capture</button>
            </div>
            <canvas id="canvas" style="display:none;"></canvas>
            <input type="hidden" id="photo" name="photo">

            <script>
                const webcamElement = document.getElementById('webcam');
                const canvasElement = document.getElementById('canvas');
                const captureButton = document.getElementById('capture');

                navigator.mediaDevices.getUserMedia({ 'video': true })
                .then(stream => {
                    webcamElement.srcObject = stream;
                });

                captureButton.addEventListener('click', () => {
                    canvasElement.width = webcamElement.videoWidth;
                    canvasElement.height = webcamElement.videoHeight;
                    const context = canvasElement.getContext('2d');
                    context.drawImage(webcamElement, 0, 0);
                    let photo = canvasElement.toDataURL('image/jpeg');
                    document.getElementById('photo').value = photo;
                });
            </script>
        """

# 이제 클래스를 인스턴스화하고 html_code를 가져올 수 있습니다.
webcam_capture = WebcamCaptureHTML()
html_code = webcam_capture.html_code
