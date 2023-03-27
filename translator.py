from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as font
import pathlib, os
import googletrans
import textblob
import pyaudio
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO #file-like object for playing the gtts speech directly
from pydub import AudioSegment
from pydub.playback import play

# current directory
current_dir = pathlib.Path(__file__).parent.resolve() # current directory

# main window
main = Tk()
main.title('Translator-Py')
# set up an icon
icon = PhotoImage(master=main, file=os.path.join(current_dir, 'images/icon.png'))
# apply the icon to the tkinter window
main.wm_iconphoto(True, icon)
# tkinter window size
main.geometry('650x330')
main.resizable(False, False)

# relative path to the image
speaker_icon = PhotoImage(file = os.path.join(current_dir, 'images/speaker-icon.png'))
swap_icon = PhotoImage(file = os.path.join(current_dir, 'images/swap.png'))
mic_icon = PhotoImage(file = os.path.join(current_dir, 'images/microphone.png'))

# get the language list and put their values in a list
languages = googletrans.LANGUAGES
language_list = list(languages.values())

def translate():
    try:
        # delete any previous translation
        translated_text.delete(1.0, END)

        # Get languages from keys
        # Get language from
        for key,value in languages.items():
            if(value == from_select.get()):
                from_lang_key = key
        # Get language to
        for key,value in languages.items():
            if(value == translate_select.get()):
                to_lang_key = key

        # Turn the text from the from box into textblob
        words = textblob.TextBlob(from_text.get(1.0, END)) # get everything in the text box from start (1.0) to the end

        # Translate the text
        words = words.translate(from_lang=from_lang_key, to=to_lang_key)

        # Put the translated text in the other box
        translated_text.insert(1.0, words)

    except Exception as err:
        messagebox.showerror("Translator", err)

def tts_from():
    for key,value in languages.items():
        if(value == from_select.get()):
            lang_key = key

    text_to_play = from_text.get(1.0, END)

    # get audio from server
    speak = gTTS(text=text_to_play, lang=lang_key, slow = False)

    # convert to file-like object
    mp3_fp = BytesIO()
    speak.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Play the sound  
    sound = AudioSegment.from_file(mp3_fp, format="mp3")
    play(sound)

def tts_translated():
    for key,value in languages.items():
        if(value == translate_select.get()):
            lang_key = key

    ttp = translated_text.get(1.0, END)

    # get audio from server
    speak_output = gTTS(text = ttp, lang=lang_key, slow = False)
    
    # convert to file-like object
    mp3_fp = BytesIO()
    speak_output.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Play the sound  
    sound = AudioSegment.from_file(mp3_fp, format="mp3")
    play(sound)

def speech_to_text():
    recogniser = sr.Recognizer()

    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = recogniser.record(source, duration=5)

        # Get from language key
        for key,value in languages.items():
            if(value == from_select.get()):
                lang_key = key

        # convert speech to text
        text = recogniser.recognize_google(audio_data, language=lang_key)
        # insert the text into the text box
        from_text.insert(1.0, text)
        
def swap_languages():
    first_lang = from_select.current()
    second_lang = translate_select.current()

    from_select.current(second_lang)
    translate_select.current(first_lang)

def clear():
    # clear text boxes
    from_text.delete(1.0, END)
    translated_text.delete(1.0, END)

# text boxes - ROW 1
from_text = Text(main, height=14, width=39)
from_text.grid(row=0, column=0, pady=5, padx=2, columnspan = 5)
from_text.insert('1.0', 'Text To Translate...')
from_text.bind("<FocusIn>", lambda args: from_text.delete('1.0', 'end'))

translated_text = Text(main, height=14, width=40)
translated_text.grid(row=0, column=5, pady=5, padx=2, columnspan = 5)
translated_text.insert('1.0', 'Translation...')
translated_text.bind("<FocusIn>", lambda args: translated_text.delete('1.0', 'end'))

######################## ROW 2
# microphone
mic_button = Button(main, image=mic_icon, command=speech_to_text, borderwidth=0)
mic_button.grid(row=1, column=0, pady=5, padx=1)

# speaker icon button
speaker_from_button = Button(main, image=speaker_icon, command=tts_from, borderwidth=0)
speaker_from_button.grid(row=1, column=1, pady=5, padx=1)

#select element
from_select = ttk.Combobox(main, width=35, value=language_list)
from_select.current(21) # English
from_select.grid(row=1, column=2, columnspan = 2)

# swap icon button - MIDDLE
swap_button = Button(main, image=swap_icon, command=swap_languages, borderwidth=0)
swap_button.grid(row=1, column=4, pady=5, padx=1, columnspan=2)

#select element
translate_select = ttk.Combobox(main, width=39, value=language_list)
translate_select.current(21)
translate_select.grid(row=1, column=6, columnspan=3)

# speaker icon button
speaker_translate_button = Button(main, image=speaker_icon, command=tts_translated, borderwidth=0)
speaker_translate_button.grid(row=1, column=9, pady=5, padx=1)

############################# ROW 3

# clear button - under the text boxes
clear_button = Button(main, text='Clear', font=('Poppins',14), command=clear, borderwidth=1, bg='#06283D', fg='white')
clear_button.grid(row=2, column=3, padx=10, columnspan = 2)

# translate button - under the text boxes
translate_button = Button(main, text='Translate', font=('Poppins',14), command=translate, borderwidth=1, bg='#06283D', fg='white')
translate_button.grid(row=2, column=5, padx=5, columnspan = 3)

if __name__ == "__main__":
	main.mainloop()