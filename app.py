import os
import streamlit as st
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, TextClip
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

# Fix ffmpeg path
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/usr/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/bin/ffprobe"

# 💅 Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #fff;
        }
        .main {
            background: linear-gradient(to right, #0f0f0f, #1c1c1c);
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton>button {
            background-color: #ff0055;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
        .stButton>button:hover {
            background-color: #cc0044;
        }
        .style-gallery {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 1rem;
        }
        .style-box {
            position: relative;
            width: 180px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .style-box:hover {
            transform: scale(1.05);
        }
        .style-thumbnail {
            width: 100%;
            border-radius: 10px;
            border: 3px solid transparent;
        }
        .style-box:hover .style-thumbnail {
            border-color: #ff0055;
        }
        .style-preview {
            display: none;
            position: absolute;
            top: 0;
            width: 100%;
            border-radius: 10px;
        }
        .style-box:hover .style-preview {
            display: block;
            z-index: 10;
        }
        .caption {
            text-align: center;
            font-size: 0.95rem;
            color: #ddd;
            margin-top: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# 🎬 VIDEO STYLES
video_styles = [
    {
        "name": "Anime Visualizer",
        "thumbnail": "https://drive.google.com/uc?id=1kl73Idu3CSVCk3lOrqBy1q_OEwTNQ3fd",
        "preview": "https://drive.google.com/uc?id=1e-FFFDndZWaKcQS5iY4uyNFHMD9yixkl",
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
        "description": "Futuristic, neon-lit cityscapes. Great for synthwave or EDM."
    },
    {
        "name": "Street Graffiti",
        "thumbnail": "https://drive.google.com/uc?id=1ZfyZm_Ay-mquuyBpXlwzTZ8ivw2Gi_q9",
        "preview": "https://drive.google.com/uc?id=1CSHAOyOP4RDTQOar8xVyrXuiQM7NeSfs",
        "description": "Animated street art. Perfect for hip-hop or underground rap."
    },
    {
        "name": "Cosmic Nebula",
        "thumbnail": "https://drive.google.com/uc?id=1BfiZREooj8C39ePfmrMO4-G6ruuoyBNW",
        "preview": "https://drive.google.com/uc?id=14cW4B1M2_dnVKB2GJnefJHQyiDxaAEtk",
        "description": "Epic space visuals. Best for chill, spacey beats."
    },
    {
        "name": "Matrix Code",
        "thumbnail": "https://drive.google.com/uc?id=1CZOHKlTu1qI4Nh-2H67mwqDlWw3RkCz8",
        "preview": "https://drive.google.com/uc?id=1e-FFFDndZWaKcQS5iY4uyNFHMD9yixkl",
        "description": "Code rain + glitch. Killer for dark techno or cyber themes."
    },
    {
        "name": "Urban Glitch",
        "thumbnail": "https://drive.google.com/uc?id=1ll7_dJ9Zr18gLjk3D6u_eJxwIkFQKtQZ",
        "preview": "https://drive.google.com/uc?id=1oS5JPDsobTVxiNdDNADZYjQjJjYfb3Sj",
        "description": "Neon, chaotic motion. Great for trap or electronic beats."
    },
    {
        "name": "VHS Retro",
        "thumbnail": "https://drive.google.com/uc?id=1Wq_9L96zxNU5dKOpw64iQ8HbTiiih4pa",
        "preview": "https://drive.google.com/uc?id=1eXd_rOi9M6AYF2yY7WOfxnoiZ0kXz3rm",
        "description": "Old-school grain & 90s nostalgia. Best for lofi or synth."
    },
]

# 🚀 App title
st.markdown("<h1 style='text-align: center;'>🔥 MP3 ➜ MP4 Social Video Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload an MP3 and image, pick a video style, and blast out a short banger for Reels, Shorts, or TikTok.</p>", unsafe_allow_html=True)

# 🎨 Style Selection with hover preview
st.markdown("### 🎨 Choose a Video Style")
selected_style = None
style_index = st.session_state.get("style_index", -1)

style_html = "<div class='style-gallery'>"
for i, style in enumerate(video_styles):
    style_html += f"""
        <div class='style-box' onclick="fetch('/?style_index={i}')">
            <img src='{style['thumbnail']}' class='style-thumbnail'/>
            <video autoplay muted loop class='style-preview'>
                <source src='{style['preview']}' type='video/mp4'>
            </video>
            <div class='caption'>{style['name']}</div>
        </div>
    """
style_html += "</div>"

st.markdown(style_html, unsafe_allow_html=True)

# 👀 File uploaders
uploaded_audio = st.file_uploader("🎵 Upload MP3", type=["mp3"])
uploaded_image = st.file_uploader("🖼️ Upload Background Image (PNG/JPG)", type=["png", "jpg", "jpeg"])

# 🔊 Generate waveform (optional eye candy)
def create_waveform(audio_path):
    audio = AudioSegment.from_mp3(audio_path)
    samples = np.array(audio.get_array_of_samples())
    plt.figure(figsize=(8, 2))
    plt.fill_between(np.arange(len(samples)), samples, color="#00f9ff", alpha=0.5)
    plt.axis("off")
    temp_wave = os.path.join(tempfile.gettempdir(), "waveform.png")
    plt.savefig(temp_wave, bbox_inches="tight", pad_inches=0)
    plt.close()
    return temp_wave

# 🎬 Process
if uploaded_audio and uploaded_image:
    style_selected = video_styles[0]  # Default to first for now
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_audio.read())
        audio_path = temp_audio.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
        temp_image.write(uploaded_image.read())
        image_path = temp_image.name

    st.markdown("🎬 Hang tight, rendering your masterpiece...")
    st.image(create_waveform(audio_path), caption="🎶 Waveform Preview")

    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration).set_fps(24)
    text_overlay = TextClip("🔥 Your Music Video 🔥", fontsize=50, color="white", font="Arial-Bold")
    text_overlay = text_overlay.set_position("center").set_duration(audio_clip.duration)

    final_video = CompositeVideoClip([image_clip, text_overlay]).set_audio(audio_clip)
    output_path = os.path.join(tempfile.gettempdir(), "final_output.mp4")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, verbose=False, logger=None)

    st.success("✅ Done! Here's your video:")
    st.video(output_path)
    st.download_button("⬇️ Download Your Video", open(output_path, "rb").read(), file_name="music_video.mp4")

