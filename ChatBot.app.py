import streamlit as st
import speech_recognition as sr
import requests
import json
import pyttsx3
import pickle
from gtts import gTTS
from io import BytesIO

# Chargement du modèle XGBoost enregistré dans un fichier pickle
with open('xgb.pkl', 'rb') as f:
    model = pickle.load(f)
    

# Obtention de la ville à partir de laquelle l'utilisateur veut obtenir la météo
# Message d'introduction
st.title("Chatbot météo")
st.write("Bienvenue sur le chatbot météo ! Vous pouvez parler ou taper le nom de votre ville ou votre code postal pour connaître les prévisions météorologiques.")

# Configuration de la reconnaissance vocale
r = sr.Recognizer()
with sr.Microphone() as source:
    st.write("Dites le nom de la ville")
    audio = r.listen(source)

# Obtention de la ville avec la reconnaissance vocale
try:
    city = r.recognize_google(audio, language='fr-FR')
    st.write(f"Vous avez demandé la météo pour la ville de {city}")
except:
    st.write("Je n'ai pas compris la ville que vous avez dit.")
    city = None
st.write(f"Vous avez demandé la météo pour la ville de {city}")

# Récupération des données météorologiques
if city:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=fr&appid=98e027721603ca32cead5457312b406a"
    response = requests.get(url)
    data = response.json()
    st.image(f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png")
    st.write(f"Conditions météorologiques: {data['weather'][0]['description']}")
    st.write(f"Température: {round(data['main']['temp'] - 273.15)}°C")
    st.write(f"Humidité: {data['main']['humidity']}%")
    st.write(f"Vitesse du vent: {data['wind']['speed']} m/s")

    # Fonction pour obtenir les prévisions météorologiques à partir d'une API
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=fr&appid=98e027721603ca32cead5457312b406a"
    response = requests.get(url)
    data1 = response.json()
    return data1
    
    # Fonction pour convertir du texte en parole
def text_to_speech(text):
    with BytesIO() as file:
        gTTS(text=text, lang='fr').write_to_fp(file)
        file.seek(0)
        return file.read()

city = st.text_input("Ville ")
submit_button = st.button("Obtenir la prévision météorologique")
        
if submit_button:
    data1 = get_weather(city)
    
    # Affichage de la réponse du chatbot et des prévisions météorologiques
    st.write(f"Conditions météorologiques: {data['weather'][0]['description']}")
    st.write(f"Température: {round(data['main']['temp'] - 273.15)}°C")
    st.write(f"Humidité: {data['main']['humidity']}%")
    st.write(f"Vitesse du vent: {data['wind']['speed']} m/s")
    
    
    # Synthèse vocale de la réponse du chatbot
    audio_file = text_to_speech(f"La prévision météorologique pour {data['name']} est {data['weather'][0]['description']} avec une température de {round(data['main']['temp'] - 273.15)} degrés Celsius, une humidité de {data['main']['humidity']} pour cent et une vitesse de vent de {data['wind']['speed']} mètres par seconde.")
    st.audio(audio_file, format='audio/mp3')

# Bouton pour effacer l'historique des discussions et recommencer une nouvelle conversation
if st.button("Effacer l'historique des discussions"):
    st.session_state.history = []

# Affichage de l'historique des discussions
if 'history' not in st.session_state:
    st.session_state.history = []
for message in st.session_state.history:
    st.write(message)
    audio_file = text_to_speech(message)
    st.audio(audio_file, format='audio/mp3')

# Ajout de nouveaux messages à l'historique des discussions
if submit_button:
    st.session_state.history.append(f"Prévision météorologique pour {data['name']}: {data['weather'][0]['description']}, température de {round(data['main']['temp'] - 273.15)}°C, humidité de {data['main']['humidity']}%, vitesse de vent de {data['wind']['speed']} m/s.")
