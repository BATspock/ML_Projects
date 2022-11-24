from Levenshtein import distance 
import moviepy.editor as mp
import whisper
import timeit
import xml.etree.ElementTree as ET
import os
import sys
import json
import matplotlib.pyplot as plt


#function to transcribe and compare
def convert_video_to_audio(video_file_path):
    #convert video mp4 to mp3
    start_time = timeit.default_timer()

    clip = mp.VideoFileClip(video_file_path)
    clip.audio.write_audiofile(video_file_path.replace(".mp4",".mp3"))
    #move converted audio file to audio folder
    audio_file = video_file_path.replace(".mp4",".mp3")
    audio_file = audio_file.split('/')[-1]
    os.replace('Data/'+audio_file,'audio/'+audio_file)
    #transcribe the audio file
    print("Time Taken to transcribe the audio file:",timeit.default_timer()-start_time)

def compare(audio_file_path, xml_path, model_type = 'tiny.en'):

    #print("Converting video to audio")
    
    print("audio file path:",'audio/'+ audio_file_path)
    print("xml file path:",xml_path)
    print('#'*50)

    #transcribe the audio file
    start_time = timeit.default_timer()
    
    model = whisper.load_model(model_type)
    result = model.transcribe('audio/'+ audio_file_path, fp16=False)

    transcription_time = timeit.default_timer() - start_time
    print("Time Taken to transcribe the audio file:",transcription_time)
    
    whisper_output = result['text'].split()
    #extract the text from the xml file

    start_time = timeit.default_timer()

    tree = ET.parse(xml_path)
    words = []
    for node in tree.findall('.//p/span'):
        words.append(node.text)

    #print("Time Taken to extract the text from the xml file:",timeit.default_timer() - start_time)

    #filter the words from xml file and whisper output

    start_timer = timeit.default_timer()

    filtered_words = []
    for word in words:
        if word == None:
            continue
        elif '[' not in word:
            if ':' not in word:
                filtered_words.append(word)

    #get sets of filtered words and whisper output
    set_whisper_output = set(whisper_output)
    set_filtered_words = set(filtered_words)
    #convert the lists to string
    whisper_output_str = ' '.join(whisper_output)
    filtered_words_str = ' '.join(filtered_words)
    print('$'*20)
    print()
    print("Number of words in the video:",len(set_whisper_output))
    print("Number of words in the xml file:",len(set_filtered_words))
    print('$'*20)
    print()
    #calculate unique words in the video and xml file
    print("Number of unique words in the video:",len(set_whisper_output - set_filtered_words))
    print("Number of unique words in the xml file:",len(set_filtered_words - set_whisper_output))
    print('$'*20)
    print()
    #print("Time Taken to process the string:",timeit.default_timer() - start_timer)

    #calculate levenshitn distance between the two strings
    start_timer = timeit.default_timer()
    print(filtered_words_str[:20])
    print(whisper_output_str[:20])
    with open(audio_file_path.split('/')[-1]+str(model_type)+'.txt', "w") as text_file:
        text_file.write(whisper_output_str.lower())
    levenshitn_distance = distance(filtered_words_str.lower(),whisper_output_str.lower())/len(filtered_words_str)
    print("Levenshtein distance between xml words and whisper output:", levenshitn_distance)
            #distance(filtered_words_str.lower(),whisper_output_str.lower())/len(filtered_words_str))
    print('$'*20)
    print()
    print("Time Taken to calculate levenshtein distance:",timeit.default_timer() - start_timer)

    print('#'*50)

    return transcription_time, levenshitn_distance, len(set_filtered_words - set_whisper_output)



#compare the video and xml files with tiny model

if __name__ == '__main__':


#    video_files = []
#    for file in os.listdir('Data/'):
#        if file.endswith('.mp4'):
#            video_files.append(file)
#    video_files.sort()

    xml_files = []
    for file in os.listdir(os.getcwd()):
        if file.endswith('.xml'):
            xml_files.append(file)
    xml_files.sort()
    #print(video_files, xml_files)

    #convert video mp4 to mp3
    #for video_file in video_files:
    #  convert_video_to_audio('Data/'+ video_file)
    
    audio_files = []
    for file in os.listdir('audio/'):
        if file.endswith('.mp3'):
            audio_files.append(file)
    audio_files.sort()

    print(xml_files, audio_files)


    TIME = []
    DISTANCE = []
    WORDS = []
#    print(audio_files)
#    tiny_time = []
#    tiny_distance = []
#    tiny_words = []
#    for i in range(len(audio_files)):
#        print("#### NEW VIDEO TINY####")
#        time , dist, words = compare(audio_files[i],xml_files[i], "tiny.en")
#        tiny_time.append(time)
#        tiny_distance.append(dist)
#        tiny_words.append(words)
#    TIME.append(tiny_time)
#    DISTANCE.append(tiny_distance)
#    WORDS.append(tiny_words)

#    base_time = []
#    base_distance = []
#    base_words = []
#    for i in range(len(audio_files)):
#        print("#### NEW VIDEO BASE####")
#        time , dist, words = compare(audio_files[i],xml_files[i], "base.en")
#        base_time.append(time)
#        base_distance.append(dist)
#        base_words.append(words)
#    TIME.append(base_time)
#    DISTANCE.append(base_distance)
#    WORDS.append(base_words)

#    small_time = []
#    small_distance = []
#    small_words = []
#    for i in range(len(audio_files)):
#        print("#### NEW VIDEO SMALL####")
#        time , dist, words = compare(audio_files[i],xml_files[i], "small.en")
#        small_time.append(time)
#        small_distance.append(dist)
#        small_words.append(words)
#    TIME.append(small_time)
#    DISTANCE.append(small_distance)
#    WORDS.append(small_words)

    medium_time = []
    medium_distance = []
    medium_words = []
    print("Medium Model")
    for i in range(len(audio_files)):
        print("#### NEW VIDEO MEDIUM ####")
        time , dist, words = compare(audio_files[i],xml_files[i], "medium.en")
        medium_time.append(time)
        medium_distance.append(dist)
        medium_words.append(words)
    TIME.append(medium_time)
    DISTANCE.append(medium_distance)
    WORDS.append(medium_words)

    #save TIME and DISTANCE in json format
    with open('time.json', 'w') as f:
        json.dump(TIME, f)
    with open('distance.json', 'w') as f:
        json.dump(DISTANCE, f)
    with open('words.json', 'w') as f:
        json.dump(WORDS, f)

    #plot the graphs
    
    plt.figure(figsize=(5,5))
    plt.scatter(TIME[0], DISTANCE[0], label = 'tiny')
#    plt.scatter(TIME[1], DISTANCE[1], label = 'base')
#    plt.scatter(TIME[2], DISTANCE[2], label = 'small')
#     plt.scatter(TIME[3], DISTANCE[3], label = 'medium')

    plt.xlabel('Time')
    plt.ylabel('Levenshtein Distance')
    plt.title('Levenshtein Distance vs Time')
    plt.legend()
    plt.savefig('levenshtein_distance_vs_time.png')

    plt.figure(figsize=(5,5))
    plt.scatter(WORDS[0], DISTANCE[0], label = 'tiny')  
#    plt.scatter(WORDS[1], DISTANCE[1], label = 'base')
#    plt.scatter(WORDS[2], DISTANCE[2], label = 'small') 
#    plt.scatter(WORDS[3], DISTANCE[3], label = 'medium')

    plt.xlabel('Number of words')
    plt.ylabel('Levenshtein Distance')
    plt.title('Levenshtein Distance vs Number of words')
    plt.legend()
    plt.savefig('levenshtein_distance_vs_words.png')
