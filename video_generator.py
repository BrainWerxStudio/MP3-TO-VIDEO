import os
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip


def create_waveform(audio_path):
    """Generate a waveform image from an MP3 file."""
    audio = AudioSegment.from_mp3(audio_path)
    samples = np.array(audio.get_array_of_samples())
    plt.figure(figsize=(10, 2))
    plt.fill_between(np.arange(len(samples)), samples, color="cyan", alpha=0.5)
    plt.axis("off")
    waveform_path = os.path.join(tempfile.gettempdir(), "waveform.png")
    plt.savefig(waveform_path, bbox_inches="tight", pad_inches=0)
    plt.close()
    return waveform_path


def generate_video(audio_path, image_path, output_path=None, overlay_text="Your Music Video"):
    """
    Generates an MP4 music video with background image, text overlay, and synced audio.
    
    Args:
        audio_path (str): Path to MP3 audio file
        image_path (str): Path to background image
        output_path (str): Optional output path (defaults to temp folder)
        overlay_text (str): Text to overlay on video

    Returns:
        str: Path to generated MP4 file
    """
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration).set_fps(24)

    text_clip = TextClip(overlay_text, fontsize=50, color='white', font='Arial-Bold')
    text_clip = text_clip.set_position('center').set_duration(audio_clip.duration)

    final_video = CompositeVideoClip([image_clip, text_clip])
    final_video = final_video.set_audio(audio_clip)

    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), "music_video_output.mp4")

    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)

    return output_path
