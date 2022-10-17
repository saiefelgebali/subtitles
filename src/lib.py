import tempfile
import os
import shutil
import uuid
from dotenv import load_dotenv
from pytube import YouTube
from pydub import AudioSegment


load_dotenv()

TEMP_PATH = './temp'
TEMP_AUDIO_FILENAME = 'audio.wav'
INPUT_VIDEO_FILENAME = 'input.mp4'
PICO_VOICE_ACCESS_KEY = os.environ.get("PICO_VOICE_ACCESS_KEY")


def clear_temp(dir):
    temp_dir = os.path.join(dir, TEMP_PATH)
    shutil.rmtree(temp_dir)


def download_youtube_video(url, outdir):
    try:
        video = YouTube(url)
    except:
        print("Connection error")

    print(f"Downloading '{video.title}'")

    stream = video.streams.get_highest_resolution()
    dir = os.path.join(outdir, str(uuid.uuid4()))
    if not os.path.exists(dir):
        os.mkdir(dir)
    filename = stream.download(dir, filename=INPUT_VIDEO_FILENAME)
    return dir, filename


def convert_to_wav(path, dir):
    sound = AudioSegment.from_file(path)
    temp_dir = os.path.join(dir, TEMP_PATH)
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    new_path = os.path.join(temp_dir, TEMP_AUDIO_FILENAME)
    sound.export(new_path, format='wav')
    return new_path


def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)


def save_file(string, filename):
    with open(filename, 'w') as f:
        f.write(string)
    return filename
