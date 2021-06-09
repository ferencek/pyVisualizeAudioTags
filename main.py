"""! 
@brief main.py
@details This is the main file of pyVisualizeMp3Tags

@author Theodoros Giannakopoulos {tyiannak@gmail.com}
"""

import csv
import sys
import argparse
import os
from tqdm import tqdm
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import audio_metadata


def list_audio_files(path_name, recursively = False):
    """! Lists all audio files in a particular folder

    \param folder path to search for audio files

    \param (\a boolean) (not) recursive search for audio files

    \returns (\a list) of full paths to audio files"""

    extensions = ('.flac','.m4a','.mp3','.mp4','.ogg','.wma')
    if recursively:
        audio_files = []
        for root, dirs, files in os.walk(path_name, followlinks=True):
            for filename in files:
                if filename.lower().endswith(extensions):
                    audio_files.append(os.path.join(root, filename))
    else:
        audio_files = [os.path.join(path_name, file)
                       for file in os.listdir(path_name) if
                         file.lower().endswith(extensions)]

    return sorted(audio_files)


def generate_word_cloud(list_of_tags, output_file):
    text = "+".join([at["genre"].lower()#.replace(" ", "_")
                     for at in list_of_tags])
    print(text)
    wordcloud = WordCloud(width=800, height=400, regexp=r"\w[\w' &-]+", collocations=False, background_color="white").generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_file)


def get_audio_tags(file_path):
    """! Gets audio tags from an audio file

    \param file_path the path to the input audio file

    \returns dict of audio tags"""
    try:
        artist = track = album = genre = ""
        metadata = audio_metadata.load(file_path)
        if metadata.tags.artist[0].strip():
            artist = metadata.tags.artist[0].strip()
        if metadata.tags.album[0].strip():
            album = metadata.tags.album[0].strip()
        if metadata.tags.title[0].strip():
            track = metadata.tags.title[0].strip()
        if metadata.tags.genre[0].strip():
            genre = metadata.tags.genre[0].strip()
        return {"artist": artist, "track": track, "album": album, "genre": genre}
    except:
        return None


def parseArguments():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-i', '--input', nargs=None, required = True,
                        help="Input audio path (folder that contains audio files)")
    parser.add_argument('-o', '--output', nargs=None, required = True,
                        help="Output figure file")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()

    audio_paths = list_audio_files(args.input, True)
    all_tags = []
    for audio_path in tqdm(audio_paths):
        cur_tag = get_audio_tags(audio_path)
        if cur_tag:
            all_tags.append(cur_tag)

    generate_word_cloud(all_tags, args.output)
