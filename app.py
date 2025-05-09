import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO
import os

def convert_video_to_audio(video_file):
    # Sauvegarder temporairement le fichier vidéo uploadé
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.read())

    # Charger la vidéo et extraire l'audio
    clip = VideoFileClip("temp_video.mp4")
    audio = clip.audio

    # Sauvegarder l'audio dans un fichier temporaire
    audio_file_path = "temp_audio.mp3"
    audio.write_audiofile(audio_file_path)

    # Lire le fichier MP3 dans un buffer BytesIO
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()

    # Nettoyage des fichiers temporaires
    clip.close()
    audio.close()
    os.remove("temp_video.mp4")
    os.remove("temp_audio.mp3")

    return BytesIO(audio_bytes)

# Interface Streamlit
st.title("Convertisseur MP4 vers MP3 🎵")

uploaded_file = st.file_uploader("Téléversez une vidéo MP4", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    if st.button("Convertir en MP3"):
        with st.spinner("Conversion en cours..."):
            audio_buffer = convert_video_to_audio(uploaded_file)
            st.success("Conversion terminée !")
            st.download_button(
                label="Télécharger le fichier MP3",
                data=audio_buffer,
                file_name="audio_converti.mp3",
                mime="audio/mpeg"
            )
