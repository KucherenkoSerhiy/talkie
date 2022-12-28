import datetime
import re

import ffmpeg
import whisper
from pytube import YouTube
import os

model = whisper.load_model("base")

youtube_video_url = "https://youtu.be/KPbq4wBPeH0"
youtube_video = YouTube(youtube_video_url)

# Get the first audio stream
audio_stream = youtube_video.streams.filter(only_audio=True).first()

# Set the file name
file_name = youtube_video.title + ".mp4"
file_name = re.sub('[^A-Za-z0-9 .]+', '', file_name)

# Download the audio stream and save it to the file
audio_stream.download(filename=file_name)

# Load the input audio file
input_audio = ffmpeg.input(file_name)

# Use the trim filter to specify the start and end times for the trimmed audio
trimmed_audio = input_audio.filter_('trim', start='00:00:10', end='00:00:20')

# Use ffmpeg.output to specify the output file and run the conversion
ffmpeg.output(trimmed_audio, file_name, overwrite_output=True).run()

print(f"analyzing {youtube_video.title}")
print("------------------------------------------------")

t1 = datetime.datetime.now()
print(f"started at {t1}")
result = model.transcribe(file_name)
t2 = datetime.datetime.now()
print(f"ended at {t2} (elapsed {t2 - t1})")

print(result["text"])
