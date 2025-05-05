import os
import streamlit as st
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, TextClip
from pydub import AudioSegment

# Set up ffmpeg path
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/usr/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/bin/ffprobe"

# Define video styles (Google Drive direct links)
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
    },
]

# Style
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #111;
            color: #fff;
        }
        .style-button {
            border: 2px solid #444;
            padding: 10px;
            border-radius: 10px;
            transition: all 0.2s ease-in-out;
        }
        .style-button:hover {
            border-color: #ff4b4b;
            background-color: #222;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 MP3 to Music Video Generator")
st.markdown("Upload an MP3 and image, then pick a video style and get a short music video ready for social media.")

# === STYLE SELECTION ===
selected_style = None
cols = st.columns(4)
for i, style in enumerate(video_styles):
    col = cols[i % 4]
    with col:
        if st.button(f"{style['name']}", key=style["name"]):
            selected_style = style
        st.image(style["thumbnail"], caption=style["name"], use_container_width=True)

# === PREVIEW SELECTED STYLE ===
if selected_style:
    st.markdown(f"### Preview: {selected_style['name']}")
    st.video(selected_style["preview"])
    st.markdown(f"*{selected_style['description']}*")
else:
    st.warning("👈 Pick a style to preview it!")

# === FILE UPLOAD ===
uploaded_audio = st.file_uploader("🎵 Upload MP3", type=["mp3"])
uploaded_image = st.file_uploader("🖼️ Upload Background Image", type=["png", "jpg", "jpeg"])
video_title = st.text_input("💬 Add Title (optional)", value="Your Music Video")

# === WAVEFORM ===
def generate_waveform(path):
    audio = AudioSegment.from_mp3(path)
    samples = np.array(audio.get_array_of_samples())
    plt.figure(figsize=(10, 2))
    plt.fill_between(np.arange(len(samples)), samples, color="cyan")
    plt.axis("off")
    output_path = os.path.join(tempfile.gettempdir(), "waveform.png")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()
    return output_path

# === GENERATE VIDEO ===
if uploaded_audio and uploaded_image and selected_style:
    st.markdown("### 🔧 Processing...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
        audio_file.write(uploaded_audio.read())
        audio_path = audio_file.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as image_file:
        image_file.write(uploaded_image.read())
        image_path = image_file.name

    try:
        waveform_path = generate_waveform(audio_path)
        st.image(waveform_path, caption="Waveform Preview")

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration).set_fps(24)

        elements = [image_clip]

        if video_title:
            txt = TextClip(video_title, fontsize=70, font='Arial-Bold', color='white')
            txt = txt.set_position("center").set_duration(audio_clip.duration)
            elements.append(txt)

        final = CompositeVideoClip(elements)
        final = final.set_audio(audio_clip)

        output_path = os.path.join(tempfile.gettempdir(), "final_video.mp4")
        final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        st.success("✅ Done! Here's your video:")
        st.video(output_path)

        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download MP4", f, "music_video.mp4", mime="video/mp4")

    except Exception as e:
        st.error(f"💥 Something broke: {e}")
