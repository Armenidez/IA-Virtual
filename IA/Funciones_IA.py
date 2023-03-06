

import webbrowser as web
import datetime
from cv2 import namedWindow
import speech_recognition as sr
import os
import keyboard
import pyjokes
import pywhatkit 
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
from translate import Translator


# Spotify credentials
client_id = 'be10e3b83fa64d478166bff785d08c3f'
client_secret = 'c0d64c0d9bd34dec84705f16b2a7aa26'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

#Traductor a japones
translator=Translator(to_lang='ja')

#Asistenete nombre
name = 'asistente'

listener = sr.Recognizer()

r=sr.Recognizer()
#print(sr.Microphone.list_microphone_names())

def IA_listen():
    #funcion que escucha el microfono y devuelve el texto
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        # r.energy_threshold()
        print("say anything : ")
        audio= r.listen(source)
        try:
            text = r.recognize_google(audio, language='es-ES')
            text = text.lower()
            print(text)
            if name in text:
                text = text.replace(name, '')
                text = text.lstrip()
                print(text)
                return text
            
        except:
            print("sorry, could not recognise")
            return ''
    
def functions():
    #Funciones de la IA
    rec = IA_listen()
    try:
        if 'reproduce' in rec:
            
            if 'youtube' in rec:
                yt = rec.replace('reproduce', '')
                yt = yt.replace('en youtube', '')
                yt = yt.replace('youtube', '')
                yt = yt.lstrip()
                
                print("reproduciendo " + yt)
                pywhatkit.playonyt(yt)
                
            elif 'spotify' in rec:
                
                music = rec.replace('reproduce', '')
                music = music.replace('en spotify', '')
                music = music.replace('spotify', '')
                music = music.lstrip()
                
                if 'de' in music:
                    
                    L_music = music.split('de')
                    name_song = L_music[0]
                    name_song = name_song.strip()
                    author = L_music[1]
                    author = author.strip()
                    q = "track:{}, artist:{}".format(name_song, author)
                    q1 = "track:{}, artist:{}".format(translator.translate(name_song), author)
                    q2 = "track:{}".format(translator.translate(name_song))
                    q3 = "artist:{}".format(author)
                    result=sp.search(q,type="track", limit=20)
                    print(q,'\n',q1, '\n', q2, '\n', q3)
                    
                    if result["tracks"]["total"] > 0:
                        web.open(result["tracks"]["items"][0]["uri"])
                    else:
                        result=sp.search(q1,type="track", limit=20)
                        if result["tracks"]["total"] > 0:
                            web.open(result["tracks"]["items"][0]["uri"])
                        else:
                            result=sp.search(q2,type="track", limit=20)
                            if result["tracks"]["total"] > 0:
                                web.open(result["tracks"]["items"][0]["uri"])
                            else:
                                result=sp.search(q3,type="track", limit=20)
                                #print(len(result["tracks"]["items"]))
                                for i in range(len(result["tracks"]["items"])):
                                    #print(result["tracks"]["items"][i]["name"], name_song, result["tracks"]["items"][i]["name" ]== name_song)
                                    if result["tracks"]["items"][i]["name"] == translator.translate(name_song) or result["tracks"]["items"][i]["name"] == name_song:
                                        web.open(result["tracks"]["items"][i]["uri"])
                                        break
                                                                
                elif 'del autor' in music:
                    L_music = music.split('del autor')
                    name_song = L_music[0]
                    name_song = name_song.strip()
                    author = L_music[1]
                    author = author.strip()
                    q = "track:{}, artist:{}".format(name_song, author)
                    q1 = "track:{}, artist:{}".format(translator.translate(name_song), author)
                    result=sp.search(q,type="track", limit=20)
                    
                    if print(result["tracks"]["total"]) == 0:
                        result=sp.search(q1,type="track", limit=20)
                        web.open(result["tracks"]["items"][0]["uri"])
                    else:
                        web.open(result["tracks"]["items"][0]["uri"])
                
                else:
                    
                    name_song = music
                    name_song = name_song.strip() 
                    q = "track:{}".format(name_song)
                    result=sp.search(q,type="track", limit=1)
                    web.open(result["tracks"]["items"][0]["uri"])
            else:

                name_song = rec
                name_song = name_song.replace("reproduce", '')
                name_song = name_song.strip() 
                q = "track:{}".format(name_song)
                result=sp.search(q,type="track", limit=1)
                web.open(result["tracks"]["items"][0]["uri"])
                        
    except:
    
        print('no entiendo')
    
    functions()

#funcion para inicializar la app
functions()
    

