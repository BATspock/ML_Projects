import whisper
import os
import timeit

#transcribe audio files and save the output as txt file in transcription folder
#if there is no transcription folder, create one

def transcribe(audio_file_path, model_type):
    #get transcription file name and get complete path by combining it with audio folder path
    transcription_file_name = os.path.basename(audio_file_path)
    transcription_file = os.path.join('new_audio', transcription_file_name)

    #transcribe audio file
    start_time = timeit.default_timer()
    
    model = whisper.load_model(model_type)
    result = model.transcribe(transcription_file, fp16=False)

    transcription_time = timeit.default_timer() - start_time
    
    print("Time Taken to transcribe the audio file:",transcription_time)
    
    whisper_output = result['text']

    #get file name without extension
    transcription_file_name_without_extension = os.path.splitext(transcription_file_name)[0]

    #save the transcription output as txt file in transcription folder
    #if there is no transcription folder, create one
    if not os.path.exists('transcription'):
        os.makedirs('transcription')

    #save the transcription output as txt file in transcription folder
    with open(os.path.join('transcription', transcription_file_name_without_extension + model_type +'.txt'), 'w') as f:
        f.write(whisper_output)

    
if __name__ == '__main__':
    #get audio files from audio folder
    audio_files = os.listdir('new_audio')

    #transcribe audio files and save the output as txt file in transcription folder
    for audio_file in audio_files:
        transcribe(audio_file, 'tiny.en')

    # for audio_file in audio_files:
    #     transcribe(audio_file, 'base.en')

    # for audio_file in audio_files:
    #     transcribe(audio_file, 'medium.en')