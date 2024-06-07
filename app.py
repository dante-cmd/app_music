from tkinter import *
from tkinter import ttk
import re
import pandas as pd
from collections import namedtuple
from pydub import AudioSegment
from pathlib import Path
import numpy as np
import subprocess

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title('App Music Rodri')
        # self.window.iconbitmap('coding_computer_pc_screen_code_icon_193925.ico')
        # self.window.iconbitmap("logo-dj-rodri.ico")
        self.window.resizable(0,0) # inmovile 0 -> False (rown), 0 --> (False)
        self.data_input_paths = []
        self.data = []

    def play(self):    
        self.frame = LabelFrame(self.window, text='INPUT DATA')
        self.frame.grid(row=0, column=0, columnspan=4, pady=10)

        # path input
        # label_input = Label(frame, text='PATH FOLDER INPUT: ')
        width = 30
        label_input = Label(self.frame, text='FOLDER INPUT: ')
        label_input.grid(row=1, column=0, sticky = "w", padx=5)
        self.input_path_entry = Entry(self.frame)
        self.input_path_entry.config(width=width)
        self.input_path_entry.grid(row=1, column=1, pady=5, padx=5, columnspan=1)
        self.input_path_entry.focus()
        #print(self.path.get())
        
        # pais input
        label_effect = Label(self.frame, text='FOLDER EFFECT: ')
        # label_effect = Label(self.frame, text='PATH FOLDER EFFECT: ')
        label_effect.grid(row=2, column=0, sticky = "w", padx=5)
        self.effect_path_entry = Entry(self.frame)
        self.effect_path_entry.config(width=width)
        self.effect_path_entry.grid(row=2, column=1,pady=5, padx=5 ,columnspan=1)


        label_effect_name = Label(self.frame, text='EFFECT NAME: ')
        # label_effect = Label(self.frame, text='PATH FOLDER EFFECT: ')
        label_effect_name.grid(row=3, column=0, sticky = "w", padx=5)
        self.effect_name_entry = Entry(self.frame)
        self.effect_name_entry.config(width=width)
        self.effect_name_entry.grid(row=3, column=1,pady=5, padx=5 ,columnspan=1)

        label_cover = Label(self.frame, text='FOLDER COVER: ')
        # label_effect = Label(self.frame, text='PATH FOLDER EFFECT: ')
        label_cover.grid(row=4, column=0, sticky="w", padx=5)
        self.cover_path_entry = Entry(self.frame)
        self.cover_path_entry.config(width=width)
        self.cover_path_entry.grid(row=4, column=1, pady=5, padx=5, columnspan=1)

        label_cover_name = Label(self.frame, text='COVER NAME: ')
        # label_effect = Label(self.frame, text='PATH FOLDER EFFECT: ')
        label_cover_name.grid(row=5, column=0, sticky="w", padx=5)
        self.cover_name_entry = Entry(self.frame)
        self.cover_name_entry.config(width=width)
        self.cover_name_entry.grid(row=5, column=1, pady=5, padx=5, columnspan=1)



        #print(self.pais.get())
        
        # label_output = Label(self.frame, text='PATH FOLDER OUTPUT: ')
        label_output = Label(self.frame, text='FOLDER OUTPUT: ')
        label_output.grid(row=6, column=0, sticky = "w", padx=5)
        self.output_path_entry = Entry(self.frame)
        self.output_path_entry.config(width=width) #
        self.output_path_entry.grid(row=6, column=1,pady=5, padx=5 ,columnspan=1)

        label_cd = Label(self.frame, text='CD NAME: ')
        label_cd.grid(row=7, column=0, sticky = "w", padx=5)
        self.label_cd_entry = Entry(self.frame)
        self.label_cd_entry.config(width=width) #
        self.label_cd_entry.grid(row=7, column=1,pady=5, padx=5 ,columnspan=1)

        # Add product
        button_read = ttk.Button(self.frame, text='READ', padding=5, width=20, command=self.read_inputs)
        button_read.grid(row = 8, column=0 , columnspan=1, padx=5, pady=5) #, sticky=W +E )

        #button_add_product = ttk.Button(self.frame, text='INSERT', command=self.add_product)
        #button_add_product.grid(row = 2, column=1) # sticky=W +E )
        button_run = ttk.Button(self.frame, text='RUN', padding=5, width=20, command=self.running)
        button_run.grid(row = 8, column=1, columnspan=1, padx=5, pady=5) #, sticky=W +E )
        #button_close = ttk.Button(self.frame, text='CLOSE', command=self.window.destroy)
        #button_close.grid(row =3, column=1) #, sticky=W +E )
        button_edit = ttk.Button(self.frame, text='EDIT', padding=5, width=20, command=self.edit_seconds)
        button_edit.grid(row = 8, column=2, columnspan=1, padx=5, pady=5) #, sticky=W +E )

        self.label_output = Label(self.frame, text='', fg='#E63946')
        self.label_output.grid(row=9, column=0, columnspan=3)
    

        # view

        self.tree = ttk.Treeview(height=10, columns=('NAME', 'FIRST', 'SECOND'), show="headings", padding=8)
        # 'FIRST', 'SECOND'
        self.tree.grid(row=4, column=0, columnspan=3)
        self.tree.heading("#0", text="Item")
        # self.tree.heading('#0', text='INDEX')
        self.tree.heading('#1', text='NAME')
        self.tree.heading('#2', text='FIRST')
        self.tree.heading('#3', text='SECOND')
        # self.tree.heading('#4', text='')

        #self.tree.insert('', 0, text='1', values=(self.path.get(), self.pais.get()))
         
    def read_inputs(self):
        if len(self.input_path_entry.get()) == 0:
            self.label_output['text'] = 'NO INPUT PATH'
        elif self.input_path_entry.get() in  self.data_input_paths:
            self.label_output['text'] = 'DUBLICATE INPUT PATH'
        else:
            path_input_songs = Path(self.input_path_entry.get())
            if not path_input_songs.exists():
                self.label_output['text'] = 'INPUT PATH NOT EXIST'
            else:
                self.label_output['text'] = ''
                self.data_input_paths.append(self.input_path_entry.get())
                for path_file in path_input_songs.glob('*'):
                    audio_format = re.search(r'.+\.(mp3|wav|aac|flac)$', path_file.name, flags=re.I|re.DOTALL)
                    if audio_format:
                        self.tree.insert("", 0, 
                                values=(path_file.name, 
                                        "", 
                                        ""))
                        self.data.append(path_file)
                        
                #array_data.append(path_file.name)
            

    def edit_seconds(self):
        selection = self.tree.selection()
        if not selection:
            self.label_output['text'] = 'NO SELECTED'
        else:
            self.label_output['text'] = ''
            self.selected= selection[0]
            current_values = self.tree.item(self.selected, "values")
            self.name_song = current_values[0]
            self.window_top = Toplevel()
            self.window_top.title = 'Edit'

            label_first = Label(self.window_top, text='FIRST:')
            label_first.grid(row=0, column=0 , sticky = "w")#, padx=5, pady=5)
            self.input_first_entry = Entry(self.window_top)
            self.input_first_entry.config(width=10)
            self.input_first_entry.grid(row=0, column=1)# pady=5, padx=5)
            self.input_first_entry.focus()


            label_second = Label(self.window_top, text='SECOND:')
            label_second.grid(row=1, column=0 , sticky = "w") #, padx=5, pady=5)
            self.input_second_entry = Entry(self.window_top)
            self.input_second_entry.config(width=10)
            self.input_second_entry.grid(row=1, column=1 ) #, pady=5, padx=5)
            # self.input_second_entry.focus()

            button_run = ttk.Button(self.window_top, text='APPLY', padding=5, width=20, command=self.apply_values)
            button_run.grid(row = 2, column=1, columnspan=1, padx=5, pady=5) #, sticky=W +E )

    def get_response(self,entry):
        search =re.search(r"^(\d{2}\:\d{2})$", entry)
        length = len(entry)
        if length == 0:
            return ""
        elif search:
            return search.group(1)
        else:
            return "ERROR"

    def apply_values(self):
        first_response = self.get_response(self.input_first_entry.get())
        second_response = self.get_response(self.input_second_entry.get())
        if (first_response == "ERROR") or (second_response == "ERROR"):
            self.label_output['text'] = 'NO VALID'
        else:
            self.tree.item(self.selected, values=(self.name_song ,first_response, second_response))
            self.label_output['text'] = ''
            self.input_first_entry.delete(0, END)
            self.input_second_entry.delete(0, END)
            self.window_top.destroy()

    
    def handle_effect(self, path_effect, name_effect):
        
        if len(path_effect)==0 and len(name_effect) == 0:
            self.label_output['text'] = "NO PATH EFFECT|NO NAME EFFECT"
        elif len(path_effect) ==0 and len(name_effect) != 0:
            self.label_output['text'] = "NO PATH EFFECT"
        elif len(path_effect) !=0 and len(name_effect) == 0:
            self.label_output['text'] = "NO NAME EFFECT"
        else:
            if not Path(path_effect).exists():
                self.label_output['text'] = "PATH EFFECT NO EXISTS"
            else:
                if not (Path(path_effect)/name_effect).exists():
                    self.label_output['text'] = "PATH EFFECT EXISTS BUT NOT NAME EFFECT"
                else:
                    self.label_output['text'] = ''
                    return Path(path_effect)/name_effect

    def handle_cover(self, path_cover:str, name_cover:str):

        if len(path_cover) == 0 and len(name_cover) == 0:
            self.label_output['text'] = "NO PATH COVER|NO NAME COVER"
        elif len(path_cover) == 0 and len(name_cover) != 0:
            self.label_output['text'] = "NO PATH COVER"
        elif len(path_cover) != 0 and len(name_cover) == 0:
            self.label_output['text'] = "NO NAME COVER"
        else:
            if not Path(path_cover).exists():
                self.label_output['text'] = "PATH COVER NO EXISTS"
            else:
                if not (Path(path_cover) / name_cover).exists():
                    self.label_output['text'] = "PATH COVER EXISTS BUT NOT NAME COVER"
                else:
                    self.label_output['text'] = ''
                    return Path(path_cover) / name_cover
    def handle_path_output(self, path_output):
        if len(path_output) == 0:
            self.label_output['text'] = "NO PATH OUTPUT"
        else:
            if not Path(path_output).exists():
                self.label_output['text'] = "PATH OUTPUT NO EXISTS"
            else:
                return Path(path_output)

    def handle_cd(self, cd_name:str):
        if len(cd_name) == 0:
            self.label_output['text'] = "NO CD NAME"
        else:
            return cd_name

    def running(self):
        response_effect = self.handle_effect(self.effect_path_entry.get(), self.effect_name_entry.get())
        response_output = self.handle_path_output(self.output_path_entry.get())
        response_cover = self.handle_effect(self.cover_path_entry.get(), self.cover_name_entry.get())
        response_cd = self.handle_cd(self.label_cd_entry.get())


        array_seconds = []
        name_seconds = namedtuple('namedtuple', ['NAME', 'FIRST', 'SECOND'])
        data = pd.Series(self.data, name='INPUT_PATH')
        data_frame = data.to_frame()
        data_frame['NAME'] = data_frame.INPUT_PATH.apply(lambda x: x.name)
        if (not self.tree.get_children()) or (not response_effect) or (not response_output) or (not response_cover) or (not response_cd):
            pass
        else:
            for item in self.tree.get_children():
                # heading = self.tree.item(item, "text")
                values = self.tree.item(item, "values")
                array_seconds.append(name_seconds(*values))

            data_seconds = pd.DataFrame(array_seconds)
            data_consol =data_frame.merge(data_seconds, on='NAME', how='outer')
            data_consol = data_consol.map(lambda x:np.NaN if x == '' else x)
            print(data_consol)
            self.add_effects(data_consol, response_output, response_effect)
            self.add_cover(data_consol, response_output, response_cd, response_cover)

    def add_effects(self, data, path_output_songs, path_effect_file):
        for path_file, name_file, first_position_time, second_position_time in data.itertuples(index=False):
            song = AudioSegment.from_file(path_file)
            sound_effect = AudioSegment.from_file(path_effect_file)

            sound_effect = sound_effect - 5  # Reduce the volume of the sound effect by 10 dB


            # Set the position (in milliseconds) where you want to insert the sound effect
            # first_position_time, second_position_time = dict_first[path_file.name], dict_second[path_file.name]


            def split_time(time):
                if pd.isna(time):
                    return time
                minute, second = time.split(':')
                return (int(minute) * 60 + int(second)) * 1000

            first_position, second_position = split_time(first_position_time), split_time(second_position_time)

            if pd.isna(second_position) and pd.isna(first_position):
                song_add_final_effect = song

            elif pd.isna(second_position) and (not pd.isna(first_position)):
                # Mix the sound effect into the song at the specified position
                # Adjust the volume of the sound effect if needed
                # Overlay the sound effect on the song
                song_add_final_effect = song.overlay(sound_effect, position=first_position)

            elif pd.isna(first_position) and (not pd.isna(second_position)):
                # Mix the sound effect into the song at the specified position
                # Adjust the volume of the sound effect if needed
                # Overlay the sound effect on the song
                song_add_final_effect = song.overlay(sound_effect, position=second_position)
            else:
                song_add_first_effect = song.overlay(sound_effect, position=first_position)
                song_add_final_effect = song_add_first_effect.overlay(sound_effect, position=second_position)

                # Export the combined audio to a new file
            if (path_output_songs/path_file.name).exists():
                # If the file already exists, delete it
                (path_output_songs/path_file.name).unlink()

            song_add_final_effect.export(path_output_songs/path_file.name, format="mp3",  bitrate="320k")
            print("Sound effect has been mixed into the song successfully!", path_file.name)

    def add_cover_image_to_mp3(self, mp3_file, cover_image, output_file):
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

    def add_cover(self, data, path_output, cd_name, path_cover_file):
        if not (path_output / cd_name).exists():
            (path_output / cd_name).mkdir()

        for path_file, name_file, *_ in data.itertuples(index=False):
        # for path_file in path_output_songs.glob('*'):
            audio_format = re.search(r'.+\.(mp3|wav|aac|flac)$', path_file.name, flags=re.I | re.DOTALL)
            if audio_format:
                path_input_absolute = str((path_output / path_file.name).absolute())
                if (path_output / cd_name / path_file.name).exists():
                    (path_output / cd_name / path_file.name).unlink()

                path_output_absolute = str((path_output / cd_name / path_file.name).absolute())
                # path_file_absolute = str(path_file.absolute())

                path_cover_absolute = str((path_cover_file).absolute())

                path_input_absolute = path_input_absolute.replace('\\', '/')
                # path_file_absolute = path_file_absolute.replace('\\', '/')
                path_cover_absolute = path_cover_absolute.replace('\\', '/')
                path_output_absolute = path_output_absolute.replace('\\', '/')

                # Add cover image to MP3 file
                self.add_cover_image_to_mp3(path_input_absolute, path_cover_absolute, path_output_absolute)


if __name__ == '__main__':

    # window = Tk()
    applications = App()
    applications.play()
    # applications.config()
    applications.window.mainloop()