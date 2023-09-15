import streamlit as st
import base64
import os

st.title("Webcam Photo Capture in Streamlit")

# User input for folder path
folder_path = st.text_input("Enter the folder path to save the photo:")

# HTML to create a video element and capture button
html_code = """
    <div style="display: flex; justify-content: center;">
        <video id="webcam" width="640" height="480" autoplay></video>
        <button id="capture" style="margin-top: 10px;">Capture</button>
    </div>
    <canvas id="canvas" style="display:none;"></canvas>

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

# Embed the HTML in the Streamlit app
st.markdown(html_code, unsafe_allow_html=True)

# Capture the photo data
photo_data = st.text_area(label="Captured Photo (base64)", height=200, key="photo")

if photo_data and folder_path:
    header, encoded = photo_data.split(",", 1)
    photo_bytes = base64.b64decode(encoded)
    
    # Save the photo to the specified folder
    file_path = os.path.join(folder_path, "captured_photo.jpg")
    with open(file_path, "wb") as f:
        f.write(photo_bytes)

    st.success(f"Photo saved to: {file_path}")
