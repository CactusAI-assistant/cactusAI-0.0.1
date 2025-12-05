import requests
import webbrowser
import re


def get_weather(city: str, api_key: str) -> str:
    """Возвращает погоду для города"""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "ru"}
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            return f"В городе {city} {weather} Температура {temp}°C Влажность {humidity}% Ветер {wind} м/с"
        return f"Ошибка: {data.get('message', 'не удалось получить погоду')}."
    except Exception:
        return "Ошибка при подключении к погодному сервису."


def open_website(url: str, msg: str = None):
    """Открывает ссылку в браузере и озвучивает сообщение"""
    webbrowser.open(url)
    if msg:
        from speech import speak
        speak(msg)


def get_first_video_id(query: str) -> str | None:
    """Возвращает ID первого видео YouTube по поисковому запросу"""
    try:
        search_url = f"https://www.youtube.com/results?search_query={query}"
        response = requests.get(search_url)
        video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", response.text)
        return video_ids[0] if video_ids else None
    except Exception:
        return None


def search_youtube(query: str):
    """Открывает YouTube по запросу"""
    url = f"https://www.youtube.com/results?search_query={query}"
    open_website(url, f"Ищу {query} на YouTube")
