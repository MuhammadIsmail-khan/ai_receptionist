import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.title("Audio Recorder")

# Inject the JavaScript code
record_audio_js = """
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", () => {
      const audioBlob = new Blob(audioChunks);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();

      // Send the audio blob to the Streamlit app
      var reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      reader.onloadend = function() {
        var base64data = reader.result;
        fetch('/upload-audio', {
          method: 'POST',
          body: JSON.stringify({ data: base64data }),
          headers: {
            'Content-Type': 'application/json'
          }
        });
      };
    });

    document.querySelector("#startRecording").addEventListener("click", () => {
      mediaRecorder.start();
    });

    document.querySelector("#stopRecording").addEventListener("click", () => {
      mediaRecorder.stop();
    });
  });
"""

# Create start and stop buttons for recording
components.html(f"""
<button id="startRecording">Start Recording</button>
<button id="stopRecording">Stop Recording</button>
<script>
{record_audio_js}
</script>
""")

# Endpoint to handle audio data
def save_audio(audio_data):
    audio_data = audio_data.split(",")[1]
    audio_bytes = base64.b64decode(audio_data)
    with open("audio_recorded.wav", "wb") as f:
        f.write(audio_bytes)

if st.experimental_get_query_params():
    if 'data' in st.experimental_get_query_params():
        save_audio(st.experimental_get_query_params()['data'][0])
        st.audio("audio_recorded.wav")
