#!/usr/bin/env python3from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import SynthesizeCallback
import pyaudio
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
authenticator = IAMAuthenticator('EKsJcbw_OxkfKKUijUqfvz6OeOVZJsu6lwzyFapbwFFW')
service = TextToSpeechV1(authenticator=authenticator)
service.set_service_url('https://gateway-lon.watsonplatform.net/text-to-speech/api')
class Play(object):
    """
    Wrapper to play the audio in a blocking mode
    """
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 22000
        self.chunk = 1024
        self.pyaudio = None
        self.stream = None

    def start_streaming(self):
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self._open_stream()
        self._start_stream()

    def _open_stream(self):
        stream = self.pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk,
            start=False
        )
        return stream

    def _start_stream(self):
        self.stream.start_stream()

    def write_stream(self, audio_stream):
        self.stream.write(audio_stream)

    def complete_playing(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self):
        SynthesizeCallback.__init__(self)
        self.play = Play()

    def on_connected(self):
        print('Opening stream to play')
        self.play.start_streaming()

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.play.write_stream(audio_stream)

    def on_close(self):
        print('Completed synthesizing')
        self.play.complete_playing()
#Housing the required elements for tts in a function
def speak(SSML_text):
    test_callback = MySynthesizeCallback()
    service.synthesize_using_websocket(SSML_text,
                                   test_callback,
                                   accept='audio/wav',
                                   voice="en-US_AllisonVoice"
                                  )
#Now intializing stt
#Welcome message on bootup
      # <express-as type=\"Apology\">
        #I am sorry to inform you that the items you requested are backordered.
        #We apologize for the inconvenience.
       #</express-as>
      #<express-as type=\"Uncertainty\">
        #We don't know when the items will become available. Maybe next week,
        #but we are not sure at this time.
      #</express-as>
      #<express-as type=\"GoodNews\">
        #But because we want you to be a satisfied customer, we are giving you
        #a 50% discount on your order!
      #</express-as>
#Main Command Sentences
#If statements
#import speech_recognition as sr
# initialization
#time.sleep(2)
#SSML_speak = """
 #  <speak><voice-transformation type="Custom" pitch="70%">Hey!!,</voice-transformation>
  #      My name is Needah, and i am an automated bot, that will help you surf the
   #     web. You can say, 'open firefox', to get started </speak>"""
#speak(SSML_speak)
reply = """<speak><emphasis-as type="GoodNews">"I got these results for you"</emphasis></speak>"""
error = """<speak><emphasis-as type=Apology">"Sorry, right now, i can only search google, and send mails, sorry fam"</emphasis></speak>""" 
r = sr.Recognizer()
mic = sr.Microphone()
browser = webdriver.Firefox()
def search_google(query):
    browser.get('http://www.google.com')
    search = browser.find_element_by_name('q')
    search.send_keys(query)
    search.send_keys(Keys.RETURN)
def facebook_login():
    browser.get('http://www.facebook.com')
    username = browser.find_element_by_id('email')
    username.send_keys('07062037265')
    password = browser.find_element_by_id('pass')
    password.send_keys('General1')
    password.submit()
def email_login():
    browser.get('http://www.gmail.com')
    username = browser.find_element_by_id('identifierId')
    username.send_keys('willdynamics@gmail.com')
    username.submit()
    time.sleep(5)
    password = browser.find_element_by_class('whsOnd zHQkBf')
    password.send_keys('generalpun')
    password.submit()
def kwasu_portal():
    browser.get('http://myportal.kwasu.edu.ng')
    username = browser.find_element_by_id('user_name')
    username.send_keys('16/67aa/081')
    password = browser.find_element_by_id('password')
    password.send_keys('salako')
    submit = browser.find_element_by_tag_name('button')
    submit.click()
def kwasu_results():
    browser.get('http://myportal.kwasu.edu.ng/student/result')
#def kwasu_portal():
#def facebook_details():
#    friend_requests = browser.find_element_by_id('fbRequestsJewel')
    
    
def activate(phrase='babe'):
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            transcript = r.recognize_google(audio)
            if transcript.lower() == phrase:
                return True
            else:
                return False
    except:
        print('Am waiting, say something')


while True:
    if activate() == True:
        try:
            speak("Hey Dee, how can I help you today?")
            with mic as source:
                print('Say Something!')
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                transcript = r.recognize_google(audio)                
                phrase = 'search google for '
                facebook = 'facebook'
                email = 'gmail'
                Reality_Conf = 'reality conference'                
                portal = 'portal'
                portal_results = 'result'
                if phrase in transcript.lower():
                    search = transcript.lower().split(phrase)[-1]
                    search_google(search)
                    speak(reply)
                elif facebook in transcript.lower():
                    facebook_login()
                    speak('Done')
                elif email in transcript.lower():
                    email_login()
                    speak('Your mails are ready')
                elif Reality_Conf in transcript.lower():
                    speak('Definitely!!, i can\'t wait')
                elif portal in transcript.lower():
                    kwasu_portal()
                    speak('Alright, am in your portal')
                elif portal_results in transcript.lower():
                    kwasu_results()
                    speak('Done')
                    
                else:
                    speak(error)
        except:
            pass
    else:
        pass    