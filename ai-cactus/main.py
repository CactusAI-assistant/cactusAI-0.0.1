from speech import speak, listen
from commands import process_command


def run_cactus():
    speak("Здравствуйте, я Кактус. Чем могу помочь?")
    try:
        while True:
            command = listen()
            if not command:
                continue
            result = process_command(command)
            if result == "exit":
                break
    except KeyboardInterrupt:
        speak("До свидания, сэр!")
        print("\nВыход из программы...")


if __name__ == "__main__":
    run_cactus()
