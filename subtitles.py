import os
import argparse
from src.lib import clear_temp, download_youtube_video
from src.video import add_subtitles
from src.words import get_words_from_video, words_file_to_word_tuples, words_to_words_file

OUT_DIR = './out'
OUTPUT_FILENAME = 'output.mp4'

parser = argparse.ArgumentParser(description="Add subtitles to YouTube videos")
parser.add_argument('-s', '--source')
parser.add_argument('-ll', '--length-limit', type=int)

if __name__ == "__main__":
    args = parser.parse_args()

    print(args)

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    dir, input_file = download_youtube_video(args.source, outdir=OUT_DIR)

    words = get_words_from_video(input_file, dir)

    words_file = words_to_words_file(
        words, dir, endpoint_sec=0.5, length_limit=args.length_limit)

    word_tuples = words_file_to_word_tuples(words_file)

    output_video = add_subtitles(
        input_file, word_tuples, os.path.join(dir, OUTPUT_FILENAME))

    clear_temp(dir)

    print(f'Exported video to: {output_video}')
