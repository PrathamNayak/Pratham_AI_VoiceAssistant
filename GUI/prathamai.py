import time
import threading
import keyboard
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import os
import subprocess as sp
import imdb
import google.generativeai as genai
from kivy.core.text import LabelBase
from kivy.uix import widget, image, label, boxlayout, textinput
from kivy.core.window import Window
from kivy import clock
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, GEMINI_API_KEY
from utils import speak, youtube, send_email, search_on_google, search_on_wikipedia, news, weather_forcast, find_my_ip
from prathamaibutton import PrathamaiButton

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

Window.clearcolor = (0, 0, 0, 1)

LabelBase.register(name='dusri', fn_regular='static/dusri.ttf')
LabelBase.register(name='mw', fn_regular='static/mw.ttf')

class Prathamai(widget.Widget):
    def __init__(self, **kwargs):
        super(Prathamai, self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0, 0, 0, 0, 0, 0, 0]
        self.volume_history_size = 140

        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH

        self.add_widget(image.Image(source='static/border.jpg', size=(1920, 1080)))
        self.circle = PrathamaiButton(size=(284.0, 284.0), background_normal='static/circle.png')
        self.circle.bind(on_press=self.start_recording)
        self.start_recording()
        self.add_widget(image.Image(source='static/centre.gif', size=(self.min_size, self.min_size),
                                    pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)))
        time_layout = boxlayout.BoxLayout(orientation='vertical', pos=(150, 900))
        self.time_label = label.Label(text='', font_size=24, markup=True, font_name='RobotoMono-Regular')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)

        clock.Clock.schedule_interval(self.update_time, 1)

        self.title = label.Label(text='[b][color=#FFFFFF]PRATHAM AI VOICE ASSISTANT[/color][/b]', font_size=42,
                                 markup=True,
                                 font_name='static/mw.ttf', pos=(920, 900))
        self.add_widget(self.title)

        self.subtitles_input = textinput.TextInput(
            text='Hi Pratham! I am your Personal Voice Assistant.',
            font_size=26,
            readonly=False,
            background_color=(0, 0, 0, 0),
            foreground_color="#FFFFFF",
            #size_hint_y=None,
            size_hint=(1, 0.2),
            height=80,
            pos=(650, 100),
            width=1200,
            font_name='static/dusri.ttf',
        )
        self.add_widget(self.subtitles_input)

        self.vrh = label.Label(text='', font_size=30, markup=True, font_name='static/mw.ttf', pos=(1450, 500))
        self.add_widget(self.vrh)
        self.vlh = label.Label(text='', font_size=30, markup=True, font_name='static/mw.ttf', pos=(300, 500))
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        keyboard.add_hotkey('`', self.start_recording)

    def listen_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        # try:
        #     print("Recognizing...")
        #     user_query = r.recognize_google(audio, language='en-in')
        #     return user_query.lower()
        # except Exception:
        #     speak("Sorry I could not understand. Can  you please repeat that?")
        #     user_query = 'None'
        try:
            print("Recognizing...")
            return r.recognize_google(audio, language="en-in")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Can you please repeat that?")
            return 'None'
        except sr.RequestError:
            speak("Sorry, the service is not available.")
            return 'None'


    #def start_recording(self):
    def start_recording(self, *args):
        print("recording started")
        threading.Thread(target=self.run_speech_recognition).start()
        print("recording ended")

    def run_speech_recognition(self):
        print('before speech rec obj')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            print("audio recorded")
        print("after speech rec obj")

        try:
            query = r.recognize_google(audio, language="en-in")
            print(f'Recognised: {query}')
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', query))
            self.handle_prathamai_commands(query.lower())

        except sr.UnknownValueError:
            print("Google speech recognition could not understand audio")

        except sr.RequestError as e:
            print(e)
        return query.lower()

    def update_time(self, dt):
        current_time = time.strftime('TIME\n\t%H:%M:%S')
        self.time_label.text = f'[b][color=00FFFF]{current_time}[/color][/b]'

    def update_circle(self, dt):
        try:
            self.size_value = int(np.mean(self.volume_history))

        except Exception as e:
            self.size_value = self.min_size
            print('Warning:', e)

        if self.size_value <= self.min_size:
            self.size_value = self.min_size
        elif self.size_value >= self.max_size:
            self.size_value = self.max_size
        self.circle.size = (self.size_value, self.size_value)
        self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)

    def update_volume(self, indata, frames, time, status):
    #def update_volume(self, indata):
        volume_norm = np.linalg.norm(indata) * 200
        self.volume = volume_norm
        self.volume_history.append(volume_norm)
        # self.vlh.text = f'''[b]{np.mean(self.volume_history)}[color=#00FF00FF]
        #         {round(self.volume_history[0], 7)}\n
        #         {round(self.volume_history[1], 7)}\n
        #         {round(self.volume_history[2], 7)}\n
        #         {round(self.volume_history[3], 7)}\n
        #         {round(self.volume_history[4], 7)}\n
        #         {round(self.volume_history[5], 7)}\n
        #         {round(self.volume_history[6], 7)}\n
        #         [/color][/b]'''
        # self.vrh.text = f'''[b]{np.mean(self.volume_history)}[color=#00FF00FF]
        #         {round(self.volume_history[0], 7)}\n
        #         {round(self.volume_history[1], 7)}\n
        #         {round(self.volume_history[2], 7)}\n
        #         {round(self.volume_history[3], 7)}\n
        #         {round(self.volume_history[4], 7)}\n
        #         {round(self.volume_history[5], 7)}\n
        #         {round(self.volume_history[6], 7)}\n
        #         [/color][/b]'''
        self.vrh.text = f'''[b][color=#00FF00FF]
        {round(self.volume_history[0], 7)}\n
        {round(self.volume_history[1], 7)}\n
        {round(self.volume_history[2], 7)}\n
        {round(self.volume_history[3], 7)}\n
        {round(self.volume_history[4], 7)}\n
        {round(self.volume_history[5], 7)}\n
        {round(self.volume_history[6], 7)}\n
        [/color][/b]'''

        self.vlh.text = self.vrh.text
        if len(self.volume_history) > self.volume_history_size:
            self.volume_history.pop(0)

    def start_listening(self):
        self.stream = sd.InputStream(callback=self.update_volume)
        self.stream.start()

    def get_gemini_response(self, query):
        try:
            response = model.generate_content(query)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini Response: {e}")
            return "I am sorry, I could not process that request."

    def handle_prathamai_commands(self, query):
        try:
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you?")
            elif "open command prompt" in query or "open cmd" in query:
                speak("opening command prompt sir")
                os.system('start cmd')
            elif "open notepad" in query:
                speak("opening notepad for you sir")
                os.system('start notepad')
            elif "open chrome" in query or "open google chrome" in query:
                speak("Opening google chrome.")
                # chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                # os.startfile(chrome_path)
                os.system('start chrome')
            elif "open vs code" in query:
                speak("Opening Visual Studio Code sir.")
                vs_code_path = "C:\\Users\\prath\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
                os.startfile(vs_code_path)
            elif "ip address" in query:
                my_ip_address = find_my_ip()
                speak(f"Your ip address is {my_ip_address}")
                print(f"Your ip address is {my_ip_address}")
            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = self.listen_command().lower()
                youtube(video)
            elif "search on google" in query:
                speak(f"What do you want to search on google?")
                google_query = self.listen_command().lower()
                search_on_google(google_query)
            elif "search on wikipedia" in query:
                speak("What do you want to search on wikipedia sir?")
                wikipedia_search = self.listen_command().lower()
                results = search_on_wikipedia(wikipedia_search)
                speak(f"According to wikipedia, {results}")
            elif "send an email" in query:
                speak("On what email address you want to send sir? Please enter in the terminal.")
                receiver_email = input("Email Address: ")
                speak("What should be the subject sir?")
                subject = self.listen_command().capitalize()
                speak("What is the message?")
                message = self.listen_command().capitalize()
                if send_email(receiver_email, subject, message):
                    speak("I have sent the email sir!")
                    print("I have sent the email sir!")
                else:
                    speak("Something went wrong! Please check the error log.")
            elif "give me news" in query:
                speak(f"I am reading the latest headlines of today, sir")
                speak(news())
            elif "weather" in query:
                #/my_ip_address = find_my_ip()
                # city = requests.get(f"https://ipapi.co/{my_ip_address}/city").text
                speak("Please enter the name of your city sir")
                city = input("Enter the name of your city: ")
                speak(f"Getting weather report of your city {city}")
                weather, temp, feels_like = weather_forcast(city)
                speak(f"The temperature is {temp}, but feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("For your convenience, I am printing weather information on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels Like: {feels_like}")
            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name: ")
                text = self.listen_command()
                movies = movies_db.search_movie(text)
                if not movies:
                    speak("Sorry, I couldn't find any movie with that name.")
                else:
                    speak(f"Searching for {text}")
                    speak(f"I found these, please wait for some time to give you the details")
                    movie = movies[0]
                    movie_id = movie.getID()
                    movie_info = movies_db.get_movie(movie_id)
                    title = movie_info.get("title", "Unknown Title")
                    year = movie_info.get("year", "Unknown Year")
                    rating = movie_info.get("rating", "No rating available")
                    plot = movie_info.get('plot outline', 'Plot summary not available')
                    cast = movie_info.get("cast", [])
                    if cast:
                        actor_names = [person['name'] for person in cast[:5]]
                        actors_formatted = ", ".join(actor_names)
                    else:
                        actors_formatted = "No cast available"
                    speak(
                        f"{title} was released in {year} and has an IMDb rating of {rating}. "
                        f"It features actors like {actors_formatted}. "
                        f"The plot summary is: {plot}."
                    )
                    print(
                        f"{title} was released in {year} and has an IMDb rating of {rating}. "
                        f"It features actors like {actors_formatted}. The plot summary is: {plot}."
                    )
            else:
                gemini_response = self.get_gemini_response(query)
                gemini_response = gemini_response.replace("*", "")
                if gemini_response and gemini_response != "I am sorry, I could not process that request.":
                    speak(gemini_response)
                    print(gemini_response)
        except Exception as e:
            speak("Something went wrong while processing the request.")
            print(e)