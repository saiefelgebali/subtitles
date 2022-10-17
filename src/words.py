from typing import Sequence, Optional
import os
from dotenv import load_dotenv
import pvleopard

from .lib import convert_to_wav, save_file

load_dotenv()

WORDS_FILENAME = 'words.txt'
PICO_VOICE_ACCESS_KEY = os.environ.get("PICO_VOICE_ACCESS_KEY")

leopard = pvleopard.create(access_key=PICO_VOICE_ACCESS_KEY)


def get_words_from_video(path, dir):
    # Using https://picovoice.ai/ API
    print("Generating subtitles...")
    audio_file = convert_to_wav(path, dir)
    _, words = leopard.process_file(audio_file)
    return words


def words_as_line(words, start_sec, end_sec):
    return f'{start_sec}-{end_sec}:{words}'


def line_as_word_tuple(line: str):
    line = line.strip()
    time, words = line.split(':')
    start_sec, end_sec = time.split('-')
    start_sec = float(start_sec)
    end_sec = float(end_sec)
    return ((start_sec, end_sec), words)


def words_to_words_file(
        words: Sequence[pvleopard.Leopard.Word],
        inputdir: str,
        endpoint_sec: float = 1.,
        length_limit: Optional[int] = 16) -> str:
    lines = []
    section = 0
    start = 0

    def add_section(end: int) -> None:
        combined_words = ' '.join(x.word for x in words[start:(end + 1)])
        line = words_as_line(
            combined_words, words[start].start_sec, words[end].end_sec)
        lines.append(line)

    for i in range(1, len(words)):
        curr = words[i]
        prev = words[i - 1]
        new_line_by_pause = curr.start_sec - prev.end_sec >= endpoint_sec
        new_line_by_length = length_limit is not None and (
            i - start) >= length_limit

        if (new_line_by_pause or new_line_by_length):
            add_section(i - 1)
            start = i
            section += 1

    add_section(len(words) - 1)

    content = "\n".join(lines)

    return save_file(content, os.path.join(inputdir, WORDS_FILENAME))


def words_file_to_word_tuples(path):
    lines = []
    with open(path) as f:
        lines = list(map(lambda x: line_as_word_tuple(x), f.readlines()))
    return lines
