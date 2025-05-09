import os 
import streamlit as st
from moviepy.editor import AudioFileClip, ImageClip, TextClip, concatenate
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
        .thumbnail-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        .thumbnail-container img {
            width: 150px;
            height: auto;
            margin: 10px;
            cursor: pointer;
            border: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .thumbnail-container img:hover {
            border: 3px solid #ff4b4b;
        }
    </style>
""", unsafe_allow_html=True)

# Video styles object (Google Drive links for thumbnail and preview)
video_styles = [
    {
        "name": "Anime Visualizer",
        "thumbnail": "https://drive.google.com/uc?id=1kl73Idu3CSVCk3lOrqBy1q_OEwTNQ3fd",  # Example thumbnail link
        "preview": "https://drive.google.com/uc?id=1e-FFFDndZWaKcQS5iY4uyNFHMD9yixkl",  # Example preview link
        "description": "Animated vibes, inspired by AMVs. Ideal for pop or K-rap."
    },
    {
        "name": "Dreamscape AI",
        "thumbnail": "https://drive.google.com/uc?id=1vNk1tWe4Bz4DTe2gdjzyefzyQX-Q3PQ5",
        "preview": "https://drive.google.com/uc?id=1z9aiuKQloJuBO0mnzGbYNcnw21z83Ndw",
        "description": "Surreal, AI-generated worlds. Works great with ambient or R&B."
    },
    {
        "name": "Cyberpunk City",
        "thumbnail": "https://drive.google.com/uc?id=1aU2oDqX5lEr7xOkwAsgATwgmFKhV8KfD",
        "preview": "https://drive.google.com/uc?id=1Xfz9DzMJwtW7VLxE5G5yJFXbZemijydD",
        "description": "Futuristic, neon-lit cityscapes. Works great with synthwave or EDM."
    },
    {
        "name": "Street Graffiti",
        "thumbnail": "https://drive.google.com/uc?id=1ZfyZm_Ay-mquuyBpXlwzTZ8ivw2Gi_q9",
        "preview": "https://drive.google.com/uc?id=1CSHAOyOP4RDTQOar8xVyrXuiQM7NeSfs",
        "description": "Bold, animated street art. Perfect for hip-hop or underground rap."
    },
    {
        "name": "Cosmic Nebula",
        "thumbnail": "https://drive.google.com/uc?id=1BfiZREooj8C39ePfmrMO4-G6ruuoyBNW",
        "preview": "https://drive.google.com/uc?id=14cW4B1M2_dnVKB2GJnefJHQyiDxaAEtk",
        "description": "Epic space visuals and nebulas. Best for chill, spacey beats."
    },
    {
        "name": "Matrix Code",
        "thumbnail": "https://drive.google.com/uc?id=1CZOHKlTu1qI4Nh-2H67mwqDlWw3RkCz8",
        "preview": "https://drive.google.com/uc?id=1e-FFFDndZWaKcQS5iY4uyNFHMD9yixkl",
        "description": "Code rain, digital effects. Killer for dark techno or cyber themes."
    },
    {
        "name": "Urban Glitch",
        "thumbnail": "https://drive.google.com/uc?id=1ll7_dJ9Zr18gLjk3D6u_eJxwIkFQKtQZ",
        "preview": "https://drive.google.com/uc?id=1oS5JPDsobTVxiNdDNADZYjQjJjYfb3Sj",
        "description": "Edgy, neon, and chaotic. Perfect for trap or electronic beats."
    },
    {
        "name": "VHS Retro",
        "thumbnail": "https://drive.google.com/uc?id=1Wq_9L96zxNU5dKOpw64iQ8HbTiiih4pa",
        "preview": "https://drive.google.com/uc?id=1eXd_rOi9M6AYF2yY7WOfxnoiZ0kXz3rm",
        "description": "Old-school grain with 90s nostalgia. Best for lofi or synth."
    }
]

# Title and introduction
st.markdown("<h1 style='text-align: center;'>🎬 MP3 ➜ MP4 Video Blaster</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Drop your audio and background, and we'll make a video sexy enough for TikTok or YouTube Shorts.</p>", unsafe_allow_html=True)

# Display the interactive selection for video style
style_names = [style["name"] for style in video_styles]
style_descriptions = {style["name"]: style["description"] for style in video_styles}
style_thumbnails = {style["name"]: style["thumbnail"] for style in video_styles}

style_selected_name = st.radio(
    "Select your video style",
    options=style_names,
    format_func=lambda x: f"{x} - {style_descriptions[x]}"
)

style_selected = next(style for style in video_styles if style["name"] == style_selected_name)

# Show preview of selected style
st.image(style_thumbnails[style_selected_name], caption=style_selected_name, use_container_width=True)
st.markdown(f"**Description**: {style_selected['description']}")
st.video(style_selected['preview'])

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

if uploaded_audio and uploaded_image and style_selected:
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
        video = concatenate([image_clip.set_audio(audio_clip), text])

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
        st.error(f"Error: {str(e)}")
