import pyttsx3
import speech_recognition as sr

# Инициализация синтезатора речи
engine = pyttsx3.init()

# Настройка голоса на русский
voices = engine.getProperty('voices')
for voice in voices:
    if "ru" in str(voice.languages).lower() or "russian" in str(voice.name).lower():
        engine.setProperty('voice', voice.id)
        break


def speak(text: str):
    """Озвучить текст"""
    engine.say(text)
    engine.runAndWait()


def listen(timeout: int = 10) -> str:
    """Слушает микрофон и возвращает текст команды"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio, language="ru-RU")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Тайм-аут. Не услышал команду.")
            return ""
        except sr.UnknownValueError:
            print("Не удалось распознать команду.")
            return ""
        except sr.RequestError:
            speak("Ошибка подключения к сервису распознавания.")
            return ""
