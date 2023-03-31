
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import PIL.Image
from setuptools import Command
from win32gui import GetForegroundWindow, ShowWindow, FindWindow, SetWindowLong, GetWindowLong
from win32con import SW_MINIMIZE, WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE
import time
import webbrowser as web
import datetime
from cv2 import namedWindow
import speech_recognition as sr
import os
import keyboard
#import pyjokes
import pywhatkit 
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
from translate import Translator
import threading
import openai

#posicion del asistente en la pantalla

global a, b
a = 250
b = 350

#Datos
global Datos

Datos=[  {"role": "system", "content": "Eres una asistente virtual eres dulce y amable, tu nombre es Nava, quiero que me ayudes con todo, quiero que simules muchas emociones y cada vez que cambies de una a otra pon un emoji"},
         ]

#OpenAI credentials

openai.api_key = "api key"
openai.organization = "orgkey"

# Spotify credentials
client_id = 'be10e3b83fa64d478166bff785d08c3f'
client_secret = 'c0d64c0d9bd34dec84705f16b2a7aa26'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

#Traductor a japones
translator=Translator(to_lang='ja')

#Asistenete nombre
name = 'asistente'

#Para que pueda escuchar 
listener = sr.Recognizer()
r=sr.Recognizer()

# Funciones para que efuncione la Ventana Principal - Ventana Asistente y funciones principales, bloquear, cambiar de imagenes

def abrir_imagen(imagen):
    imagen = PIL.Image.open(imagen)
    w=6992
    h=4961
    
    global size
    size = 50
    #print(size*h/w)
    imagen = imagen.resize((size,int(size*h/w)), PIL.Image.Resampling.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen

def toggle_drag(event):
    global can_drag
    can_drag = not can_drag
    
    if not can_drag:
        setClickthrough(main)
        #Input_Text(None)
        cerrar_ventana_opciones(None)   
    else:
        CancelsetClickthrough(main)

def on_click(event):
    global dx, dy
    global dx2, dy2
    global dx3, dy3
    if can_drag:
        # Guardar la distancia entre la posicion del mouse y la esquina superior izquierda de la ventana
        dx, dy = event.x_root-main.winfo_rootx(), event.y_root-main.winfo_rooty()
        if Flag_Ventana_opciones:
            dx2, dy2 = event.x_root-main2.winfo_rootx(), event.y_root-main2.winfo_rooty()
            #print("1")
            
    else:
        setClickthrough(main)

def on_drag(event):
        
    if can_drag:
        # move the main window
        main.geometry(f"+{min(max(event.x_root-dx, -30),1600)}+{min(max(event.y_root-dy, -10), 750)}")
        if Flag_Text_Box:
            if not izquierda:
                ventana_BT.geometry(f"+{min(max(main.winfo_rootx()+60, 0), 1630)}+{max(min(main.winfo_rooty()-45, 1700), -100)}")
                #print("ventana_BT", ventana_BT.winfo_rootx(), ventana_BT.winfo_rooty())
            else:
                ventana_BT.geometry(f"+{min(max(main.winfo_rootx()-80, -80), 1630)}+{max(min(main.winfo_rooty()-45, 1700), -100)}")
        
        if Flag_Ventana_opciones:
            valor_1 = event.y_root-dy2
            if arriba == False:
                #print("main", main.winfo_rootx(), main.winfo_rooty())
                #print("main2", main2.winfo_rootx(), main2.winfo_rooty())
                #main2.geometry(f"+{min(max(event.x_root-dx2, -26), 1500)}+{max(min(valor_1, 1020), 300)}")
                main2.geometry(f"+{int(min(max(main.winfo_rootx()+350/2-225, -26), 1500))}+{max(min(main.winfo_rooty()+300,1020),-20)}")
            else:
                #print("main2", main2.winfo_rootx(), main2.winfo_rooty())
                main2.geometry(f"+{int(max(min(main.winfo_rootx()+350/2-225, 1500),-26))}+{max(main.winfo_rooty()-50,-10)}")
                #main2.geometry(f"+{min(max(event.x_root-dx2, -26), 1500)}+{max(min(valor_1, 750), -10)}")                         

def opacidad(opacidad):
    
    main.attributes("-alpha", opacidad)
    
def Imagen_Asistente(Gesto):
    global Im2
    Im1 = PIL.Image.open(Gesto)
    Im1 = Im1.resize((weight,int(Height)), PIL.Image.Resampling.LANCZOS)
    Im2 = ImageTk.PhotoImage(Im1)
    Cambiar_Imagen(Im2)    

def Cambiar_Imagen(Gesto):
    Ventana_Asistente.configure(image=Gesto)
    
def Abrir_menu(event):
    
    try:
        menu_principal.tk_popup(event.x_root, event.y_root, 0)
    finally:
        menu_principal.grab_release()
    pass

def Alternar_gestos(event):
    global contador
    #Lista que tienen todos los gestos del asistente
    L_Gesto = [Assistant_Sadica, Assistant_Molesta, Assistant_Triste, Assistant_Main, Assistant_Feliz, Assistant_Sonrojo]
    contador += 1
    #print(contador)
    if len(L_Gesto) == contador:
        contador=0
        Imagen_Asistente(L_Gesto[0])
    else:
        Imagen_Asistente(L_Gesto[contador])

def setClickthrough(main, window="Ventana Principal"):
    #Click a traves de la venta super util
    # make a function for i can click in other windows trought the program and other for cancel this
    global Style_default
    global styles
    hwnd = FindWindow(None, window)
    styles = GetWindowLong(hwnd, GWL_EXSTYLE)
    styles |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    #print(styles)
    print(SetWindowLong(hwnd, GWL_EXSTYLE, styles))

def CancelsetClickthrough(main, window="Ventana Principal"):

    hwnd = FindWindow(None, window)
    stylesNew = GetWindowLong(hwnd, GWL_EXSTYLE)
    #print(styles)
    StylesNew = Style_default
    print(SetWindowLong(hwnd, GWL_EXSTYLE, StylesNew))

def Flag_Abrir(event):
    
    global Flag_Ventana_opciones
    Flag_Ventana_opciones = not Flag_Ventana_opciones
    
    if Flag_Ventana_opciones == True:
        Abrir_Ventana_Opciones(None)

    else:
        main2.destroy()

def Block_RightClick(event):
    if can_drag:
       Flag_Abrir(None)
       
def cerrar_ventana_opciones(event):
    global Flag_Ventana_opciones
    
    main2.destroy()
    Flag_Ventana_opciones = False

def Cambiar_Image_Dialogo(event):
    
    Lista_Dialogo = [Text_Box, Text_Box_Espejo]
    
    if not izquierda:
        return Abrir_Imagenes_Dialogo(Lista_Dialogo[0])
    
    else:
        return Abrir_Imagenes_Dialogo(Lista_Dialogo[1])
     
def Abrir_Imagenes_Dialogo(img):
    global var2
    W_I = 350
    H_I = W_I*712/800
    var1                 = PIL.Image.open(img)
    var1                 = var1.resize((W_I,int(H_I)), PIL.Image.Resampling.LANCZOS)
    var2                 = ImageTk.PhotoImage(var1)
    return var2

def Abrir_Ventana_TB(event):
    global Flag_Text_Box
    
    if not Flag_Text_Box:
        Ventana_Text_Box(None)
    else:
        Cerrar_Ventana_TB(None)
        Ventana_Text_Box(None)
    Flag_Text_Box = True
    
def Cerrar_Ventana_TB(event):
    global Flag_Text_Box
    Flag_Text_Box = False
    ventana_BT.destroy()

def type_text():
    # use 'global' to allow the function to access these variables
    global index
    global placeholder
    global text_var
    global label
    global ventana_BT
    global Flag_Text_Box
    #Ventana_Text_Box(None)
   
    try:
        # concat the placeholder with the next character in 'chat_str'
        placeholder += chat_str[index]
        # set 'text_var' to update the label automatically
        text_var.set(placeholder)
        # go to the next index (character) in 'chat_str'
        index += 1
        # call this function again after 150mS
        # (change this number to modify the typing speed)
        ventana_BT.after(120, type_text)
    except IndexError:  # when you run out of characters...
        #print("ror")
        ventana_BT.after(1000, ventana_BT.destroy)
        Flag_Text_Box = False

def Insertar_texto(texto):
    global chat_str
    chat_str = texto
    chat_str = encontrar_espacio_2(chat_str)
    chat_str = chat_str + ".."
    print(chat_str)
    Abrir_Ventana_TB(None)

def encontrar_espacio(var_t, index):
    texto2 = var_t
    for i in reversed(range(index)):
        if texto2[i] == " ":
            texto2 = texto2[:i] + "\n" + texto2[i+1:]
            return texto2
        
def encontrar_espacio_2(var_t):
    texto = var_t
    widht_of_TB = 17
    if widht_of_TB < len(texto):
        if texto[widht_of_TB] != " ":
            texto = encontrar_espacio(texto, widht_of_TB)
        elif texto[widht_of_TB] == " ":
            texto = texto[:widht_of_TB] + "\n" + texto[widht_of_TB+1:]
    
    for i in range(len(texto)):
        if texto[i] == "\n":
            if i+widht_of_TB < len(texto) and texto[i+widht_of_TB] != " ":
                texto = encontrar_espacio(texto, i+widht_of_TB)
            elif i+widht_of_TB < len(texto) and texto[i+widht_of_TB] == " ":
                texto = texto[:i+widht_of_TB] + "\n" + texto[i+widht_of_TB+1:]
    return texto

def Cerrar_Aplicacion(event):

    global Flag_Ventana_opciones
    global Flag_Text_Box
    global Escuchar, Continuar_Ejecucion
    global main, main2
    
    Escuchar = False
    Continuar_Ejecucion = False

    if Flag_Ventana_opciones:
        print("procedo axd")
        main.destroy()
    
    if Flag_Text_Box:
        Cerrar_Ventana_TB(None)

    main.quit()
        
# Funciones para que escuche el programa

def IA_listen():

    global Continuar_Ejecucion
    global Escuchar
    
    while Escuchar and Continuar_Ejecucion:
    
        #funcion que escucha el microfono y devuelve el texto
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.9)
            # r.energy_threshold()
            #Insertar_texto("Escuchando.")
            print("Escuchando.")
            audio= r.listen(source)
            try:
                text = r.recognize_google(audio, language='es-ES')
                text = text.lower()
                print(text)

                if name in text:
                    text = text.replace(name, '')
                    text = text.lstrip()
                    functions(text)

                print("escuchando.")
                
            except:
                print("Disculpa, no puedo entender")
                pass
    
def functions(text):
    global yt
    global music
    global Escuchar
    #Funciones de la IA
    rec = text
    try:
        if 'reproduce' in rec:
            
            if 'youtube' in rec:
                yt = rec.replace('reproduce', '')
                yt = yt.replace('en youtube', '')
                yt = yt.replace('youtube', '')
                yt = yt.strip()
                
                Insertar_texto("reproduciendo en youtube: " + yt)
                #print("reproduciendo " + yt)
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
                    #print(q,'\n',q1, '\n', q2, '\n', q3)
                    
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
                    Insertar_texto("reproduciendo: " + name_song)
                                                                
                elif 'del autor' in music:
                    L_music = music.split('del autor')
                    name_song = L_music[0]
                    name_song = name_song.strip()
                    author = L_music[1]
                    author = author.strip()
                    q = "track:{}, artist:{}".format(name_song, author)
                    q1 = "track:{}, artist:{}".format(translator.translate(name_song), author)
                    q2 = "track:{}".format(translator.translate(name_song))
                    q3 = "artist:{}".format(author)
                    result=sp.search(q,type="track", limit=20)
                    #print(q,'\n',q1, '\n', q2, '\n', q3)
                    
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
                    
                    Insertar_texto("reproduciendo: " + name_song)
                
                else:
                    
                    name_song = music
                    name_song = name_song.strip() 
                    q = "track:{}".format(name_song)
                    result=sp.search(q,type="track", limit=1)
                    web.open(result["tracks"]["items"][0]["uri"])
                    Insertar_texto("reproduciendo: " + result['tracks']['items'][0]['name'] + " de " + result['tracks']['items'][0]['artists'][0]['name'])
            else:
                name_song = rec
                name_song = name_song.replace('reproduce', '')
                name_song = name_song.strip() 
                q = "track:{}".format(name_song)
                result=sp.search(q,type="track", limit=1)
                web.open(result["tracks"]["items"][0]["uri"])
                print(name_song)
                Insertar_texto("reproduciendo: " + result['tracks']['items'][0]['name'] + " de " + result['tracks']['items'][0]['artists'][0]['name'])
    

        elif 'pausa' in rec or 'play' in rec:
            keyboard.press_and_release("play/pause media")
            #keyboard.press_and_release("next track")   
                     
        elif 'siguiente' in rec or 'next' in rec:
            keyboard.press_and_release("next track")
        
        elif 'anterior' in rec or 'previous' in rec:
            keyboard.press_and_release("previous track")           

        elif 'cerrar' in rec:

            #Insertar_texto("Chau")
            #time.sleep(3)
            Cerrar_Aplicacion(None)

        else:
            message = rec
            #print("YO: " + message)
            Send_Message(message)
            
        
            
    except:
    
        print('no entiendo')

# Funciones de OpenAI

def Send_Message(New_Dato):
    global Datos
    
    Datos.append({"role": "user", "content": New_Dato})
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = Datos
    )

    Mensaje = response['choices'][0]['message']['content']
    Mensaje = Mensaje.replace("\n\n", " ")
    Mensaje = Mensaje.replace("\n", " ")

    Insertar_texto(Mensaje)

    #Insertar_texto('''¡Por supuesto! 😄 ¿Por qué los pájaros siempre están tan comunicativos?🦜Porque ¡siempre tuitean! 😂''')

# Funciones y Ventanas principales  

def Ventana_Asisente():
    global Height
    global main
    global Ventana_Asistente 
    global Continuar_Ejecucion

    main=tk.Tk()
    #Cargar imagen de botones

    main.title("Ventana Principal")
    main.geometry("350x450+" + "300" + "+" + "30")
    main.configure(background="DarkSlateGray")
    global weight, height
    weight=300
    Height=weight*4/3
    Asistente = PIL.Image.open(Assistant_Main)
    Asistente = Asistente.resize((weight,int(Height)), PIL.Image.Resampling.LANCZOS)
    Asistente_Img = ImageTk.PhotoImage(Asistente)

    Ventana_Asistente = tk.Label(main, image = Asistente_Img, bg='DarkSlateGray')
    Ventana_Asistente.place(x = 24, y = 10, width = weight, height = Height)

    # Crear un menu de opciones
    global menu_principal
    menu_principal = tk.Menu(main, tearoff=0)
    menu_principal.add_checkbutton(label="Bloquear", command=lambda : toggle_drag(None))

    #Cambiar gestos del asistente
    Gesto_menu = tk.Menu(main, tearoff=0)
    Gesto_menu.add_radiobutton(label="Normal"   , command=lambda : Imagen_Asistente(Assistant_Main))
    Gesto_menu.add_radiobutton(label="Feliz"    , command=lambda : Imagen_Asistente(Assistant_Feliz))
    Gesto_menu.add_radiobutton(label="Triste"   , command=lambda : Imagen_Asistente(Assistant_Triste))
    Gesto_menu.add_radiobutton(label="Sadica"   , command=lambda : Imagen_Asistente(Assistant_Sadica))
    Gesto_menu.add_radiobutton(label="Molesta"  , command=lambda : Imagen_Asistente(Assistant_Molesta))
    Gesto_menu.add_radiobutton(label="Sonrojo"  , command=lambda : Imagen_Asistente(Assistant_Sonrojo))
    menu_principal.add_cascade(label="Gestos"   , menu=Gesto_menu)

    #cambiar la opacidad de la ventana
    Opacidad_Menu = tk.Menu(menu_principal, tearoff=0)
    Opacidad_Menu.add_radiobutton(label="10%"   , command=lambda : opacidad(0.1))
    Opacidad_Menu.add_radiobutton(label="20%"   , command=lambda : opacidad(0.2))
    Opacidad_Menu.add_radiobutton(label="30%"   , command=lambda : opacidad(0.3))
    Opacidad_Menu.add_radiobutton(label="40%"   , command=lambda : opacidad(0.4))
    Opacidad_Menu.add_radiobutton(label="50%"   , command=lambda : opacidad(0.5))
    Opacidad_Menu.add_radiobutton(label="60%"   , command=lambda : opacidad(0.6))
    Opacidad_Menu.add_radiobutton(label="70%"   , command=lambda : opacidad(0.7))
    Opacidad_Menu.add_radiobutton(label="80%"   , command=lambda : opacidad(0.8))
    Opacidad_Menu.add_radiobutton(label="90%"   , command=lambda : opacidad(0.9))
    Opacidad_Menu.add_radiobutton(label="100%"  , command=lambda : opacidad(1))

    menu_principal.add_cascade(label="Opacidad", menu=Opacidad_Menu)
    menu_principal.add_separator()
    menu_principal.add_command(label="Exit", command=main.quit)
    
    
    
    main.wm_attributes("-transparentcolor", 'DarkSlateGray')
    main.wm_attributes("-topmost", True)
    #main.wm_attributes('-disabled', True)
    main.wm_attributes("-alpha", 0.6)
    main.overrideredirect(1)
    main.bind("<Button-1>", on_click)
    main.bind("<B1-Motion>", on_drag)
    main.bind("<Button-3>", Block_RightClick)
    #main.bind("<F2>", functions) # function key to lock and unlock movement
    
    main.mainloop()

def Abrir_Ventana_Opciones(event):
    global arriba
    global main2
    global Flag_Ventana_opciones

    Flag_Ventana_opciones = True

    main2 = tk.Toplevel()
    main2.configure(background='dark slate gray')
    main2.geometry("450x70")
    
    if main.winfo_rooty() < 670:
        main2.geometry(f"+{int(min(max(main.winfo_rootx()+350/2-225, -26), 1500))}+{main.winfo_rooty()+300}")
        arriba = False
    else:
        main2.geometry(f"+{int(min(main.winfo_rootx()+350/2-225, 1500))}+{main.winfo_rooty()-50}")
        arriba = True
        #324+400=724
        #734/2=369 
        #450-369

        # Creamos una nueva ventana donde poner distintas configuraciones
        #ventana_opciones = tk.Frame(main2, bg = 'white')

    I_boton_cerrar          = abrir_imagen(Cerrar)
    I_boton_cerrar_chiquito = abrir_imagen(Cerrar_chiquito)
    I_configuraciones       = abrir_imagen(Configuraciones)
    I_gestos                = abrir_imagen(Gestos)
    I_unlock                = abrir_imagen(Unlock_B)

    color1 = 'Black'
        #crear una ventana blanca
    ventana_blanca = tk.Frame(main2, bg = color1)
    ventana_blanca.place(x = 25, y = 10, width = 400, height = 50)

        #Botones
    ventana_opciones_cerrar             = tk.Label(main2, image = I_boton_cerrar, bg=color1)
    ventana_opciones_cerrar.bind('<Button-1>', lambda event: Cerrar_Aplicacion(None))

    ventana_opciones_cerrar_chiquito    = tk.Label(main2, image = I_boton_cerrar_chiquito,  bg=color1)
    ventana_opciones_cerrar_chiquito.bind('<Button-1>', lambda event: cerrar_ventana_opciones(None))
    #ventana_opciones_cerrar_chiquito.bind('<Button-1>', lambda event: main2.destroy())
    ventana_opciones_configuraciones    = tk.Label(main2, image = I_configuraciones,        bg=color1)
    ventana_opciones_configuraciones.bind('<Button-1>', Abrir_menu)   
    
    ventana_opciones_gestos             = tk.Label(main2, image = I_gestos,                 bg=color1)
    ventana_opciones_gestos.bind('<Button-1>', Alternar_gestos)
    
    ventana_opciones_Unlock             = tk.Label(main2, image = I_unlock,                 bg=color1)
    ventana_opciones_Unlock.bind('<Button-1>', toggle_drag)
        
    ventana_opciones_cerrar.place           (x=25                  , y=10+9)
    ventana_opciones_cerrar_chiquito.place  (x=25+size*5           , y=10+9)
    ventana_opciones_configuraciones.place  (x=25+size*2           , y=10+9)
    ventana_opciones_gestos.place           (x=25+size*3           , y=10+9)
    ventana_opciones_Unlock.place           (x=25+size*4           , y=10+9)
    
    #main2.bind('<B1-Motion>', on_drag2)

    main2.wm_attributes("-transparentcolor", "dark slate gray")
    main2.wm_attributes("-topmost", True)
        #que no tenga bordes
    main2.overrideredirect(1)
    main2.wm_attributes("-alpha", 0.5)
    main2.mainloop()

def Ventana_Text_Box(event):
    #Ventana De Text box
    global ventana_BT
    global Box_Texto
    global Flag_Text_Box
    global izquierda
    global chat_str
    global placeholder
    global index
    global text_var
    global label
    
    I_Text_Box                 = PIL.Image.open(Text_Box)
    I_Text_Box                 = I_Text_Box.resize((350,int(350*712/800)), PIL.Image.Resampling.LANCZOS)
    I_Text_Box_Image           = ImageTk.PhotoImage(I_Text_Box)
    
    Flag_Text_Box = True
    
    ventana_BT = tk.Toplevel()
    ventana_BT.title("Ventana Text Box")
    
    if main.winfo_rootx() > 1500:
        ventana_BT.geometry("350x350+"+str(main.winfo_rootx()-80)+"+"+str(main.winfo_rooty()-45))
        izquierda = True
    else:
        ventana_BT.geometry("350x350+"+str(main.winfo_rootx()+60)+"+"+str(main.winfo_rooty()-45))
        izquierda = False
    
    ventana_BT.configure(background="gray")
            
    Box_Texto = tk.Label(ventana_BT, image = Cambiar_Image_Dialogo(None), bg="gray")
    Box_Texto.place(x=0, y =0)
       
    # Agregar texto
    text_var = tk.StringVar()
    label = tk.Label(ventana_BT, textvariable=text_var, font=("Hack Nerd Font", 15),fg="darkblue", bg="pink", width=17, height=2, anchor="s")
    
    if not izquierda:
        label.place(x=65, y=135)
    else:
        label.place(x=90, y=135)

    # index represents the character index in 'chat_str'
    index = 0
    # we need an empty string to store the typed out string as it updates
    placeholder = ''
    type_text()
    #Box_Texto.bind('<Button-1>', lambda event: Abrir_Ventana_Texto(None))
    #chat_str = "amigos"
    '''  hwnd = FindWindow(None, "Ventana Text Box")
    styles = GetWindowLong(hwnd, GWL_EXSTYLE)
    #print(styles)
    styles |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    #print(styles)
    print(SetWindowLong(hwnd, GWL_EXSTYLE, styles))'''

    
    #Box_Texto.bind("F2", abrir_Ventana_texto)
    #global Style_default
    #global styles
    
    #ventana_BT.wm_attributes("-transparentcolor", "pink")
    ventana_BT.wm_attributes("-topmost", 1)
    ventana_BT.wm_attributes("-transparentcolor", "gray")
    ventana_BT.wm_attributes("-alpha", 0.9)
    ventana_BT.overrideredirect(1)
    
    ventana_BT.mainloop()


#puede moverse TRUE/FALSE
can_drag = True

#Bandera de ventana opciones y texto
Flag_Ventana_opciones = False
Flag_Text_Box = False

#Contador de gestos
contador = 0

#Izquierda o derecha
izquierda = False
abajo = False

#Que funcione la escucha
Escuchar = True

#Gestos del Asistente
Gesto_Actual= "Main.png"
MainGesto   = "Main_chiqito.png"
Feliz       = "Feliz.png"
Triste      = "Triste.png"
Sadica      = "Sadica.png"
Molesta     = "Enojo_chiqito.png"
Sonrojo     = "Sonrojo.png"

# Cargar todos los gestos del asistente
scriptpath          = os.path.abspath(__file__) 
scriptdir           = os.path.dirname(scriptpath) 
Assistant_Main      = os.path.join(scriptdir, MainGesto) 
Assistant_Feliz     = os.path.join(scriptdir, Feliz)
Assistant_Triste    = os.path.join(scriptdir, Triste)
Assistant_Sadica    = os.path.join(scriptdir, Sadica)
Assistant_Molesta   = os.path.join(scriptdir, Molesta)
Assistant_Sonrojo   = os.path.join(scriptdir, Sonrojo)
Cerrar              = os.path.join(scriptdir, "iconos", "Cerrar.png")
Cerrar_chiquito     = os.path.join(scriptdir, "iconos", "Cerrar_chiquito.png")
Configuraciones     = os.path.join(scriptdir, "iconos", "Configuraciones.png")
Gestos              = os.path.join(scriptdir, "iconos", "Gestos.png")
Unlock_B            = os.path.join(scriptdir, "iconos", "Unlock.png")
Text_Box            = os.path.join(scriptdir, "Dialogo", "text_box.png")
Text_Box_Espejo     = os.path.join(scriptdir, "Dialogo", "text_box_espejo.png")


#LLamada para la app 

if __name__ == "__main__":
    
    global Gui, Funciones
    global Continuar_Ejecucion

    Continuar_Ejecucion = True

    Gui = threading.Thread(target=Ventana_Asisente, name="Gui")
    Funciones = threading.Thread(target=IA_listen, name="Funciones")
    
    Funciones.start()
    Gui.start()

    #Insertar_texto("Escuchando.")
    
