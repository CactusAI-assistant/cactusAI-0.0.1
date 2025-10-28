import pyttsx3
import speech_recognition as sr
import time
import subprocess
import webbrowser
import re
import requests


# Инициализация синтезатора речи
engine = pyttsx3.init()

# Установка голосового движка на русский язык
voices = engine.getProperty('voices')
for voice in voices:
    #print(f"Имя голоса: {voice.name}, Язык: {voice.languages}, ID: {voice.id}")
    if 'Fred' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Функция для озвучивания текста
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для распознавания речи
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)  # Установите тайм-аут на 10 секунд
            return recognizer.recognize_google(audio, language="ru-RU").lower()
        except sr.WaitTimeoutError:
            print("Тайм-аут. Не услышал команду.")
            return ""
        except sr.RequestError:
            speak("Ошибка подключения. Попробуйте позже.")
            return ""
        except sr.UnknownValueError:
            print("Не удалось распознать команду.")
            return ""


# Функция для распознования погоды любой страны
def get_weather(city, api_key):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            result = (
                f"В городе {city} сейчас {weather}. "
                f"Температура {temp} градусов. "
                f"Влажность {humidity} процентов. "
                f"Скорость ветра {wind} метров в секунду."
            )
            return result
        elif data.get("message") == "city not found":
            return f"Город {city} не найден. Попробуйте снова."
        else:
            return "Ошибка получения данных о погоде."
    except:
        return "Произошла ошибка при подключении к погодному сервису."


# Функция для поиска видео на YouTube
def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)
    speak(f"Открываю YouTube ищу {query}.")

# Функция для автоматического воспроизведения видео по ссылке
def play_youtube_video(video_id):
    # Формируем URL видео
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    webbrowser.open(video_url)
    speak(f"Открываю видео. Приятного просмотра!")

# Функция для извлечения ID первого видео из результатов поиска YouTube
def get_first_video_id(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    try:
        response = requests.get(search_url)
        video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", response.text)
        if video_ids:
            return video_ids[0]
        else:
            speak("Не удалось найти видео по вашему запросу.")
            return None
    except Exception as e:
        print(f"Ошибка при поиске видео: {e}")
        speak("Произошла ошибка при поиске видео.")
        return None


#Остановка кода
def run_cactus():
    speak("Здраствуйте, я Cactus. Чем могу помочь?")

    api_key = "d3ec09af6eb533ba44ce928a1516f3f0"  # ← ВСТАВЬ СВОЙ КЛЮЧ OpenWeatherMap

    while True:
        command = listen()

        if any(keyword in command for keyword in ["пока", "стоп", "buy", "спасибо"]):
            speak("К вашим услугам Сэр!")
            break
        elif any(keyword in command for keyword in ["какое время", "который час", "сколько время"]):
            current_time = time.strftime("%H:%M")
            speak(f"Текущее время {current_time} Сэр!")
        elif "Cactus" in command:
            speak("Да Сэр?!.")

        elif "погода в" in command:
            city = command.split("погода в")[-1].strip()
            if city:
                weather_info = get_weather(city, api_key)
                speak(weather_info)
            else:
                speak("Пожалуйста, укажите город.")

        elif "открой youtube" in command:
            speak("Открываю Ютуб.")
            speak("Хотите посмотреть новые видео, Сэр!?")
            webbrowser.open("https://www.youtube.com")
        elif "включи видео" in command:
            # Извлекаем запрос из команды
            video_query = command.replace("включи видео", "").strip()
            if video_query:
                # Получаем ID первого видео по запросу
                video_id = get_first_video_id(video_query)
                if video_id:
                    play_youtube_video(video_id)
                else:
                    speak("Пожалуйста, скажите, какое видео вы хотите посмотреть.")
            
        elif "открой telegram" in command:
            speak("Открываю Телеграмм.")
            speak("Приятного общения Сэр!")
            webbrowser.open("https://web.telegram.org/")
            #subprocess.run(['open', '-a', 'Telegram']) Для Mac
            #subprocess.run(['start', 'Telegram'], shell=True) #Для Windows
        elif "открой twitch" in command:
            speak("Открываю Твич.")
            webbrowser.open("https://www.twitch.tv/")
        elif "открой discord" in command:
            speak("Открываю Дискорд.")
            speak("Хорошо провести время Сэр!")
            subprocess.run(['open', '-a', 'Discord'])
            #subprocess.run(['start', 'Discord'], shell=True) #Для Windows
        elif "включи браузер" in command:
            speak("Да сэр!")
            speak("Открываю браузер.")
            subprocess.run(['open', '-a', 'Google Chrome'])
            #subprocess.run(['start', 'Google Chrome'], shell=True) #Для Windows
        elif "открой spotify" in command:
            speak("Открываю Спотифай.")
            speak("Зажигайте Сэр!")
            webbrowser.open("https://open.spotify.com/")
        elif "включи яндекс" in command:
            speak("Да сэр!")
            speak("Открываю Яндекс браузер.")
            subprocess.run(['open', '-a', 'Yandex'])
            #subprocess.run(['start', 'Yandex'], shell=True) #Для Windows
        elif "открой проект" in command:
            speak("Да сэр!")
            speak("Открываю Пайчарм.")
            speak("Удачной работы!")
            subprocess.run(['open', '-a', 'PyCharm CE'])
            #subprocess.run(['start', 'PyCharm CE'], shell=True) #Для Windows
        elif "открой CapCut" in command:
            speak("Да сэр!")
            speak("Открываю КэпКат.")
            subprocess.run(['open', '-a', 'CapCut'])
            #subprocess.run(['start', 'CapCut'], shell=True) #Для Windows
        elif "открой whatsapp" in command:
            speak("Да сэр!")
            speak("Открываю WhatsApp.")
            speak("Хорошего общения, Сэр!")
            #subprocess.run(['open', '-a', 'WhatsApp']) Для Mac
            #subprocess.run(['start', 'WhatsApp'], shell=True) #Для Windows
            webbrowser.open("https://web.whatsapp.com/")
        elif "найди в интернете" in command:
                    search_query = command.replace("найди в интернете", "").strip()
                    if search_query:
                        speak(f"Ищу {search_query} в интернете.")
                        search_url = f"https://www.google.com/search?q={search_query}"
                        #search_url = f"https://yandex.ru/search/?text={search_query}" для Яндекс
                        webbrowser.open(search_url)
                        
        elif "включи музыку" in command:
            speak("Включаю музыку.")
            speak("Приятного прослушивания Сэр!")
            subprocess.run(['open', '-a', 'Music'])
            #subprocess.run(['start', 'Telegram'], shell=True) #Для Windows
        elif "включи finder" in command:
            speak("Включаю Финдер Сэр!.")
            speak("Хорошей работы")
            subprocess.run(['open', '-a', 'Finder'])
            #subprocess.run(['start', 'Telegram'], shell=True) #Для Windows
        elif "взлом" in command:
            speak("Вас понял! Начинаю взлом Пентагона! Сэр.")
        elif "я вернулся" in command:
            speak("С возращением!")
            speak("Не хотите послушать музыку! Сэр.")
        else:
            print("")

if __name__ == "__main__":
    run_cactus()
