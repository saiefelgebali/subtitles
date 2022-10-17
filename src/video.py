from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip


def add_subtitles(input_path, words_tuples, output_path):
    print("Exporting video...")

    video = VideoFileClip(input_path)

    def generator(txt): return TextClip(txt, font='Calibri-Bold',
                                        fontsize=32, color='yellow', stroke_color="black", stroke_width=1, method="caption", size=video.size)

    subtitles = SubtitlesClip(words_tuples, generator)

    subtitles = subtitles.set_position(("center", "center"))

    result = CompositeVideoClip([video, subtitles])

    result.write_videofile(output_path)

    video.close()

    return os.path.abspath(output_path)
