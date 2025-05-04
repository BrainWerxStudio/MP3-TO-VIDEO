import os
import streamlit as st
from moviepy.editor import AudioFileClip, ImageClip, TextClip
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from PIL import Image

# 🛠 Force MoviePy to use pre-installed ffmpeg on Streamlit Cloud
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/usr/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/bin/ffprobe"

# 💅 Custom CSS for dark glassy style
st.markdown("""
    <style>
        .main {
            background: radial-gradient(circle at top left, #1f1f1f, #000000);
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 1rem;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
        .stButton>button:hover {
            background-color: #e63c3c;
            color: #fff;
        }
        .stDownloadButton>button {
            background-color: #28a745;
            color: white;
            border-radius: 1rem;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
        .stDownloadButton>button:hover {
            background-color: #218838;
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# Video styles object
video_styles = [
    {
        "name": "Urban Glitch",
        "thumbnail": "/thumbnails/glitch.gif",
        "preview": "/previews/glitch.mp4",
        "description": "Edgy, neon, and chaotic. Perfect for trap or electronic beats."
    },
    {
        "name": "VHS Retro",
        "thumbnail": "/thumbnails/vhs.gif",
        "preview": "/previews/vhs.mp4",
        "description": "Old-school grain with 90s nostalgia. Best for lofi or synth."
    },
    {
        "name": "Anime Visualizer",
        "thumbnail": "/thumbnails/anime.gif",
        "preview": "/previews/anime.mp4",
        "description": "Animated vibes, inspired by AMVs. Ideal for pop or K-rap."
    },
    {
        "name": "Dreamscape AI",
        "thumbnail": "/thumbnails/ai.gif",
        "preview": "/previews/ai.mp4",
        "description": "Surreal, AI-generated worlds. Works great with ambient or R&B."
    },
    {
        "name": "Cyberpunk City",
        "thumbnail": "/thumbnails/cyberpunk.gif",
        "preview": "/previews/cyberpunk.mp4",
        "description": "Futuristic, neon-lit cityscapes. Works great with synthwave or EDM."
    },
    {
        "name": "Street Graffiti",
        "thumbnail": "/thumbnails/graffiti.gif",
        "preview": "/previews/graffiti.mp4",
        "description": "Bold, animated street art. Perfect for hip-hop or underground rap."
    },
    {
        "name": "Cosmic Nebula",
        "thumbnail": "/thumbnails/nebula.gif",
        "preview": "/previews/nebula.mp4",
        "description": "Epic space visuals and nebulas. Best for chill, spacey beats."
    },
    {
        "name": "Matrix Code",
        "thumbnail": "/thumbnails/matrix.gif",
        "preview": "/previews/matrix.mp4",
        "description": "Code rain, digital effects. Killer for dark techno or cyber themes."
    }
]

# Title and introduction
st.markdown("<h1 style='text-align: center;'>🎬 MP3 ➜ MP4 Video Blaster</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Drop your audio and background, and we'll make a video sexy enough for TikTok or YouTube Shorts.</p>", unsafe_allow_html=True)

# Allow users to choose a video style
st.markdown("### Choose a Video Style")
style_options = [style['name'] for style in video_styles]
selected_style = st.selectbox("Select a Style", style_options)

# Display thumbnail and description of the selected style
style = next(style for style in video_styles if style['name'] == selected_style)
st.image(style["thumbnail"], caption=f"Style Preview: {style['name']}", use_column_width=True)
st.write(f"**Description**: {style['description']}")

# Upload MP3 and background image
uploaded_audio = st.file_uploader("🎵 Upload your MP3", type=["mp3"])
uploaded_image = st.file_uploader("🖼️ Upload Background Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Function to generate waveform visualization
def create_waveform(audio_path):
    audio = AudioSegment.from_mp3(audio_path)
    samples = np.array(audio.get_array_of_samples())
    plt.figure(figsize=(10, 2))
    plt.fill_between(np.arange(len(samples)), samples, color="cyan", alpha=0.5)
    plt.axis("off")
    waveform_path = os.path.join(tempfile.gettempdir(), "waveform.png")
    plt.savefig(waveform_path, bbox_inches="tight", pad_inches=0)
    plt.close()
    return waveform_path

if uploaded_audio and uploaded_image:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_audio.read())
        audio_path = temp_audio.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
        temp_image.write(uploaded_image.read())
        image_path = temp_image.name

    st.markdown("🎧 Processing your masterpiece... hang tight.")
    progress = st.progress(0)

    try:
        progress.progress(10)
        # Create waveform preview
        waveform_path = create_waveform(audio_path)
        st.image(waveform_path, caption="🎶 Audio Waveform Preview", use_column_width=True)
        
        progress.progress(30)
        audio_clip = AudioFileClip(audio_path)
        progress.progress(50)
        
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration).set_fps(24)
        
        # Add Text Overlay
        text = TextClip("Your Music Video", fontsize=50, color='white', font='Arial-Bold')
        text = text.set_position('center').set_duration(audio_clip.duration)

        progress.progress(70)
        video = image_clip.set_audio(audio_clip).fx('CompositeVideoClip', [text])

        output_path = os.path.join(tempfile.gettempdir(), "output_video.mp4")
        progress.progress(90)
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        progress.progress(100)

        st.success("✅ MP4 video created successfully!")
        st.video(output_path)

        st.markdown("### ⬇️ Download your video")
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Music Video 🎥",
                data=f,
                file_name="music_video.mp4",
                mime="video/mp4"
            )

    except Exception as e:
        st.error(f"💣 Something exploded: {e}")
