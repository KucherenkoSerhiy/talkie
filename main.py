import datetime
import re
import subprocess

import ffmpeg
import whisper
from pytube import YouTube

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

# Store the output of the ffmpeg command
trimmed_file_name = 'trimmed_' + file_name

# Use ffmpeg.output to specify the output file and run the conversion
command = ['ffmpeg', '-i', file_name, '-y', '-f', 'mp3', '-c:a', 'libmp3lame', '-ab', '192k', '-ar', '44100']
command.extend(['-ss', '00:00:10', '-to', '00:00:20', trimmed_file_name])
subprocess.run(command)

# Read the contents of the temporary file into the trimmed_audio object
trimmed_audio.data = subprocess.check_output(command)

print(f"analyzing {youtube_video.title}")
print("------------------------------------------------")

t1 = datetime.datetime.now()
print(f"started at {t1}")

model = whisper.load_model("base")
result = model.transcribe(trimmed_file_name)
t2 = datetime.datetime.now()

print(f"ended at {t2} (elapsed {t2 - t1})")

print(result["text"])
