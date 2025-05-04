import streamlit as st
from pathlib import Path

# --- Setup ---
st.set_page_config(page_title="MP3 to Music Video", layout="wide")

video_styles = [
    {
        "name": "Urban Glitch",
        "thumbnail": "thumbnails/glitch.gif",
        "preview": "previews/glitch.mp4",
        "description": "Edgy, neon, and chaotic. Perfect for trap or electronic beats."
    },
    {
        "name": "VHS Retro",
        "thumbnail": "thumbnails/vhs.gif",
        "preview": "previews/vhs.mp4",
        "description": "Old-school grain with 90s nostalgia. Best for lofi or synth."
    },
    {
        "name": "Anime Visualizer",
        "thumbnail": "thumbnails/anime.gif",
        "preview": "previews/anime.mp4",
        "description": "Animated vibes, inspired by AMVs. Ideal for pop or K-rap."
    },
    {
        "name": "Dreamscape AI",
        "thumbnail": "thumbnails/ai.gif",
        "preview": "previews/ai.mp4",
        "description": "Surreal, AI-generated worlds. Works great with ambient or R&B."
    },
    {
        "name": "Cyberpunk City",
        "thumbnail": "thumbnails/cyberpunk.gif",
        "preview": "previews/cyberpunk.mp4",
        "description": "Futuristic, neon-lit cityscapes. Works great with synthwave or EDM."
    },
    {
        "name": "Street Graffiti",
        "thumbnail": "thumbnails/graffiti.gif",
        "preview": "previews/graffiti.mp4",
        "description": "Bold, animated street art. Perfect for hip-hop or underground rap."
    },
    {
        "name": "Cosmic Nebula",
        "thumbnail": "thumbnails/nebula.gif",
        "preview": "previews/nebula.mp4",
        "description": "Epic space visuals and nebulas. Best for chill, spacey beats."
    },
    {
        "name": "Matrix Code",
        "thumbnail": "thumbnails/matrix.gif",
        "preview": "previews/matrix.mp4",
        "description": "Code rain, digital effects. Killer for dark techno or cyber themes."
    },
]

st.title("🎧 MP3 to Music Video Generator")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])
if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

# --- Style Selection ---
st.subheader("🔥 Choose Your Vibe")
cols = st.columns(4)
selected_style = None

for i, style in enumerate(video_styles):
    with cols[i % 4]:
        st.image(style["thumbnail"], caption=style["name"])
        if st.button(f"Select {style['name']}", key=style["name"]):
            selected_style = style

if selected_style:
    st.info(f"Selected style: {selected_style['name']}")

# --- Generate Button ---
if uploaded_file and selected_style:
    if st.button("🎬 Generate Music Video"):
        with st.spinner("Generating video... please wait"):
            # Simulate processing
            import time
            time.sleep(3)
            st.success("✅ Your video is ready!")

            # Show the mock preview
            st.video(selected_style["preview"])
else:
    st.warning("Upload an MP3 and choose a style to enable generation.")
