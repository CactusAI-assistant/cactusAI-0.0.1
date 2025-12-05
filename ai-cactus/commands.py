import time
import subprocess
from speech import speak
import webbrowser
from utils import get_weather, open_website, get_first_video_id

API_KEY = "d3ec09af6eb533ba44ce928a1516f3f0"


def process_command(command):
    """Обрабатывает голосовую команду"""

    if any(k in command for k in ["пока", "стоп", "спасибо", "bye"]):
        speak("К вашим услугам!")
        return "exit"
    if any(keyword in command for keyword in ["какое время", "который час", "сколько время"]):
        current_time = time.strftime("%H:%M")
        speak(f"Текущее время {current_time} Сэр!")
    elif "ты здесь?" in command:
        speak("Да, слушаю вас!")

    elif "погода в" in command:
        city = command.split("погода в")[-1].strip()
        if city:
            info = get_weather(city, API_KEY)
            speak(info)
        else:
            speak("Пожалуйста, укажите город.")
        return

    elif "открой youtube" in command:
        speak("Открываю Ютуб.")
        webbrowser.open("https://www.youtube.com")
    if "включи видео" in command:
        query = command.replace("включи видео", "").strip()
        video_id = get_first_video_id(query)
        if video_id:
            open_website(f"https://www.youtube.com/watch?v={video_id}", "Открываю видео.")
        else:
            speak("Видео не найдено.")
            return
    elif "открой telegram" in command:
        speak("Открываю Телеграмм.")
        speak("Приятного общения")
        webbrowser.open("https://web.telegram.org/")
        # subprocess.run(['open', '-a', 'Telegram']) Для Mac
        # subprocess.run(['start', 'Telegram'], shell=True) #Для Windows
    elif "открой twitch" in command:
        speak("Открываю Твич.")
        webbrowser.open("https://www.twitch.tv/")
    elif "открой discord" in command:
        speak("Открываю Дискорд")
        speak("Хорошо провести время")
        subprocess.run(['open', '-a', 'Discord'])
        # subprocess.run(['start', 'Discord'], shell=True) #Для Windows
    elif "включи гугл" in command:
        speak("Хорошо")
        speak("Открываю google браузер.")
        subprocess.run(['open', '-a', 'Google Chrome'])
        # subprocess.run(['start', 'Google Chrome'], shell=True) #Для Windows
    elif "открой spotify" in command:
        speak("Открываю Спотифай.")
        webbrowser.open("https://open.spotify.com/")
    elif "включи яндекс" in command:
        speak("Хорошо")
        speak("Открываю Яндекс браузер.")
        subprocess.run(['open', '-a', 'Yandex'])
        # subprocess.run(['start', 'Yandex'], shell=True) #Для Windows
    elif "открой проект" in command:
        speak("Конечно")
        speak("Удачной работы!")
        subprocess.run(['open', '-a', 'Visual Studio Code'])
        # subprocess.run(['start', 'PyCharm CE'], shell=True) #Для Windows
    elif "открой обсидиан" in command:
        speak("Открываю Обсидиан.")
        subprocess.run(['open', '-a', 'Obsidian'])
        # subprocess.run(['start', 'CapCut'], shell=True) #Для Windows
    elif "открой whatsapp" in command:
        speak("Открываю WhatsApp.")
        speak("Хорошего общения")
        # subprocess.run(['open', '-a', 'WhatsApp']) Для Mac
        # subprocess.run(['start', 'WhatsApp'], shell=True) #Для Windows
        webbrowser.open("https://web.whatsapp.com/")
    elif "найди в интернете" in command:
        search_query = command.replace("найди в интернете", "").strip()
        if search_query:
            speak(f"Ищу {search_query} в интернете.")
            search_url = f"https://www.google.com/search?q={search_query}"
            # search_url = f"https://yandex.ru/search/?text={search_query}" для Яндекс
            webbrowser.open(search_url)
    elif "включи музыку" in command:
        speak("Включаю музыку.")
        subprocess.run(['open', '-a', 'Music'])
        # subprocess.run(['start', 'Telegram'], shell=True) #Для Windows
    elif "включи finder" in command:
        speak("Включаю Финдер")
        subprocess.run(['open', '-a', 'Finder'])
        # subprocess.run(['start', 'Telegram'], shell=True) #Для Windows
    elif "взлом" in command:
        speak("Вас понял!")
    elif "я вернулся" in command:
        speak("С возращением!")
    else:
        print("")
