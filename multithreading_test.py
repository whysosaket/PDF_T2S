import PyPDF2
import pyttsx3
from pynput import keyboard
import threading

with open('uhv.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    engine = pyttsx3.init()

    speed = 15000
    engine.setProperty('rate', speed)

    def on_press(key):
        global speed
        try:
            if key == keyboard.Key.space:
                if engine.isBusy():
                    engine.stop()
                else:
                    engine.runAndWait()
            elif key == keyboard.Key.up:
                speed += 50
                engine.setProperty('rate', speed)
            elif key == keyboard.Key.down:
                speed -= 50
                engine.setProperty('rate', speed)
            elif key == keyboard.Key.esc:
                engine.stop()
                return False
        except AttributeError:
            pass

    def run_engine():
        engine.runAndWait()

    def listen_keyboard():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    engine_thread = threading.Thread(target=run_engine)
    engine_thread.start()
    listener_thread = threading.Thread(target=listen_keyboard)
    listener_thread.start()

    for page in range(num_pages):
        pdf_page = pdf_reader.pages[page]
        page_text = pdf_page.extract_text()
        engine.say(page_text)
        run_engine()

        if not listener_thread.is_alive():
            break

    engine.stop()
    listener_thread.join()
