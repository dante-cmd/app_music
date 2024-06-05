from pydub import AudioSegment
from pathlib import Path
import pandas as pd
import re
import mutagen.id3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import subprocess


path_init = Path()
path_effect = Path('effect')
path_input_songs = Path('input songs')
path_output_songs = Path('output songs')
path_cover = Path("cover")
cd_name = 'DJ RODRI'


name_effect = 'dog-barking-70772.mp3'
name_cover = 'mario_bros.jpg'


def read_all_songs():
    array_data = []
    for path_file in path_input_songs.glob('*'):

        audio_format = re.search(r'.+\.(mp3|wav|aac|flac)$', path_file.name, flags=re.I|re.DOTALL)
        if audio_format:
            array_data.append(path_file.name)
    data = pd.DataFrame({"NAME":array_data})
    data['FIRST'] = pd.NaT
    data['SECOND'] = pd.NaT
    data.to_excel("data.xlsx", index=False)

def add_effects():
    data = pd.read_excel("data.xlsx", dtype={'NAME': str, 'FIRST': str, 'SECOND': str}, index_col='NAME')
    dict_first = dict(data.FIRST)
    dict_second = dict(data.SECOND)

    # Load the song and the sound effect
    for path_file in path_input_songs.glob('*'):
        audio_format = re.search(r'.+\.(mp3|wav|aac|flac)$', path_file.name, flags=re.I|re.DOTALL)
        if audio_format:
            print(path_file.name)
            song = AudioSegment.from_file(path_file)
            sound_effect = AudioSegment.from_file(path_effect/name_effect)

            sound_effect = sound_effect - 5  # Reduce the volume of the sound effect by 10 dB


            # Set the position (in milliseconds) where you want to insert the sound effect
        
            first_position_time, second_position_time = dict_first[path_file.name], dict_second[path_file.name]
    

            def split_time(time):
                if pd.isna(time):
                    return time
                minute, second = time.split(':')
                return (int(minute) * 60 + int(second)) * 1000
            
            first_position, second_position = split_time(first_position_time), split_time(second_position_time)
                    
            if pd.isna(second_position):
                # Mix the sound effect into the song at the specified position
                # Adjust the volume of the sound effect if needed

                # Overlay the sound effect on the song
                song_add_final_effect = song.overlay(sound_effect, position=first_position)
            else:
                song_add_first_effect = song.overlay(sound_effect, position=first_position)
                song_add_final_effect = song_add_first_effect.overlay(sound_effect, position=second_position)
            

                # Export the combined audio to a new file
            if (path_output_songs/path_file.name).exists():
                    # If the file already exists, delete it
                (path_output_songs/path_file.name).unlink()
                
            song_add_final_effect.export(path_output_songs/path_file.name, format="mp3",  bitrate="320k")
            print("Sound effect has been mixed into the song successfully!", path_file.name)


def add_cover_image_to_mp3(mp3_file, cover_image, output_file):
    # Construct the ffmpeg command
   
    command = (
        f'ffmpeg -y -i "{mp3_file}" -i "{cover_image}" -map 0 -map 1 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" "{output_file}"')

    
    # Run the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Cover image added successfully")
        print("Output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing command")
        print("Error Output:", e.stderr.decode())


def add_cover():
    if not (path_init/cd_name).exists():
        (path_init/cd_name).mkdir()

    for path_file in path_output_songs.glob('*'):
        audio_format = re.search(r'.+\.(mp3|wav|aac|flac)$', path_file.name, flags=re.I|re.DOTALL)
        if audio_format:
            path_init_absolute = str((path_init/cd_name/path_file.name).absolute())
            path_file_absolute = str(path_file.absolute())
            path_cover_absolute = str((path_cover/name_cover).absolute())
            print(path_file_absolute, path_cover_absolute)
            path_file_absolute = path_file_absolute.replace('\\', '/')
            path_cover_absolute = path_cover_absolute.replace('\\', '/')
            path_init_absolute = path_init_absolute.replace('\\', '/')

            # Add cover image to MP3 file
            add_cover_image_to_mp3(path_file_absolute, path_cover_absolute, path_init_absolute)

if __name__ == '__main__':
    # 
    # 5000 :5seg
    read_all_songs()
    response = input('Se ha creado el archivo data.xlsx para añadir los momentos de los efectos, escribe [s] para continuar')
    response = response.lower()
    if response == 's':
        add_effects()
        add_cover()