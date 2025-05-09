import streamlit as st
import subprocess
from io import BytesIO
import os
import tempfile

# Cette ligne doit être tout en haut
st.set_page_config(page_title="Convertisseur MP4 vers MP3", page_icon="🎵")

def convert_video_to_audio(video_file):
    # Créer des fichiers temporaires pour la vidéo et l'audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        temp_video_path = temp_video.name

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio_path = temp_audio.name
    temp_audio.close()

    # Lancer ffmpeg via subprocess avec overwrite (-y)
    command = [
        "ffmpeg", "-y",  # Overwrite automatiquement
        "-i", temp_video_path,
        "-vn", "-acodec", "libmp3lame",
        temp_audio_path
    ]
    subprocess.run(command, check=True)

    # Lire le fichier audio dans un buffer
    with open(temp_audio_path, "rb") as f:
        audio_bytes = f.read()

    # Nettoyage
    os.remove(temp_video_path)
    os.remove(temp_audio_path)

    return BytesIO(audio_bytes)

# Interface Streamlit
st.image("logo_googleworkspace.png", width=200)
st.title("Convertisseur MP4 vers MP3 🎵")

uploaded_file = st.file_uploader("Téléversez une vidéo MP4", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    if st.button("Convertir en MP3"):
        with st.spinner("Conversion en cours..."):
            try:
                audio_buffer = convert_video_to_audio(uploaded_file)
                st.success("Conversion terminée !")
                st.download_button(
                    label="Télécharger le fichier MP3",
                    data=audio_buffer,
                    file_name="audio_converti.mp3",
                    mime="audio/mpeg"
                )
            except subprocess.CalledProcessError as e:
                st.error("Erreur lors de l'exécution de ffmpeg. Détails :")
                st.code(e)
            except Exception as e:
                st.error("Une erreur s'est produite pendant la conversion :")
                st.code(str(e))
