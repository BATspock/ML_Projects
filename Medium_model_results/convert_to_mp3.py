# convert audio files to mp3
import os
from pydub import AudioSegment


def convert_to_mp3(audio_file_path):
    #get auido file name
    audio_file_name = os.path.basename(audio_file_path)
    #combine audio file name with raw_audio folder path
    #to get the full path of the audio file
    audio_file = os.path.join('raw_audio', audio_file_name)

    #convert audio file to mp3

    #get audio file name without extension
    audio_file_name_without_extension = os.path.splitext(audio_file_name)[0]

    #get audio file extension
    audio_file_extension = os.path.splitext(audio_file_name)[1]

    #convert audio file to mp3 and save in audio folder
    if audio_file_extension == '.wav':
        sound = AudioSegment.from_wav(audio_file)
        sound.export(os.path.join('audio', audio_file_name_without_extension + '.mp3'), format="mp3")

    elif audio_file_extension == '.m4a':
        sound = AudioSegment.from_file(audio_file, format="m4a")
        sound.export(os.path.join('new_audio', audio_file_name_without_extension + '.mp3'), format="mp3")
       


if __name__ == '__main__':

    #get audio files from raw_audio folder
    audio_files = os.listdir('raw_audio')

    #for each audio file in raw_audio folder
    for audio_file in audio_files:
        print("Converting " + audio_file + " to mp3")
        convert_to_mp3(audio_file)

    print('Done')

