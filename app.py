import streamlit as st
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/usr/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/bin/ffprobe"

from moviepy.editor import AudioFileClip, ImageClip
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment

def create_waveform_video(audio_path, output_path, duration=10):
    # Convert mp3 to wav for waveform analysis
    sound = AudioSegment.from_mp3(audio_path)
    wav_temp = audio_path.replace(".mp3", ".wav")
    sound.export(wav_temp, format="wav")

    samplerate, data = wavfile.read(wav_temp)
    data = data[:samplerate*duration]  # Crop to duration if needed
    if len(data.shape) > 1:
        data = data[:, 0]  # Mono

    # Generate waveform image
    plt.figure(figsize=(10, 4))
    plt.plot(data, color='hotpink')
    plt.axis('off')
    img_temp = wav_temp.replace(".wav", "_waveform.png")
    plt.savefig(img_temp, bbox_inches='tight', pad_inches=0)
    plt.close()

    # Create video from image
    clip = ImageClip(img_temp).set_duration(duration).set_fps(24)

    # Add audio to the video
    audio_clip = AudioFileClip(audio_path).subclip(0, duration)
    clip = clip.set_audio(audio_clip)

    # Export
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def main():
    st.title("🎵 MP3 to MP4 Music Video Maker")
    uploaded_file = st.file_uploader("Upload your MP3", type="mp3")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            audio_path = tmp.name

        output_path = audio_path.replace(".mp3", ".mp4")
        st.info("Creating your music video, hang tight...")

        try:
            create_waveform_video(audio_path, output_path)
            st.success("Video created!")
            with open(output_path, 'rb') as f:
                st.download_button("Download MP4", f, file_name="music_video.mp4")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
