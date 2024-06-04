from pydub import AudioSegment
from pathlib import Path
import re

path_effect = Path('effect')
path_input_songs = Path('input songs')
path_output_songs = Path('output songs')

name_effect = 'dog-barking-70772.mp3'

def add_effects(possitions:tuple):

    # Load the song and the sound effect
    for path_file in path_input_songs.glob('*'):
        audio_format = re.search(r'.+\.(mp3|wav|aac|flac)$', path_file.name, flags=re.I|re.DOTALL)
        print(audio_format.group(1))
        if audio_format:
            song = AudioSegment.from_file(path_file)
            sound_effect = AudioSegment.from_file(path_effect/name_effect)

            # Set the position (in milliseconds) where you want to insert the sound effect
            first_position, second_position = possitions
            

            # Mix the sound effect into the song at the specified position
            # Adjust the volume of the sound effect if needed
            sound_effect = sound_effect - 5  # Reduce the volume of the sound effect by 10 dB

            # Overlay the sound effect on the song
            song_add_first_effect = song.overlay(sound_effect, position=first_position)
            song_add_second_effect = song_add_first_effect.overlay(sound_effect, position=second_position)

            # Export the combined audio to a new file
            song_add_second_effect.export(path_output_songs/path_file.name, format="mp3",  bitrate="320k")

            print("Sound effect has been mixed into the song successfully!", path_file.name)

if __name__ == '__main__':
    # 
    # 5000 :5seg
    add_effects((5000, 30_000))