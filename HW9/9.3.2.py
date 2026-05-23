import keyboard
import os



class KeyboardListener:
    def update(self, key: str):
        raise NotImplementedError("Слід реалізувати метод update у підкласах.")


class KeyLogger(KeyboardListener):
    def update(self, key: str):
        print(f"[Натиснуто]: {key}")


class KeyFileLogger(KeyboardListener):

    def __init__(self, filename="key_log.txt"):
        self.filename = filename

    def update(self, key: str):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(f"{key}\n")

class KeyboardSpy:
    def __init__(self):
        self._listeners = []

    def register_listener(self, listener: KeyboardListener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: KeyboardListener):
        if listener in self._listeners:
            self._listeners.remove(listener)

    def _notify_listeners(self, key: str):
        for listener in self._listeners:
            listener.update(key)

    def main(self):
        print("KeyboardSpy запущено. Натисніть 'Ctrl + Q' для завершення.")
        while True:
            try:
                event = keyboard.read_event()

                if event.event_type == keyboard.KEY_DOWN:
                    key = event.name

                    if keyboard.is_pressed("ctrl") and key == "q":
                        print('\nFinished!')
                        break

                    self._notify_listeners(key)
            except Exception as e:
                print(f"Помилка: {e}")
                break

if __name__ == "__main__":
    keyboardSpy = KeyboardSpy()

    console_logger = KeyLogger()
    file_logger = KeyFileLogger("spy_history.txt")

    keyboardSpy.register_listener(console_logger)
    keyboardSpy.register_listener(file_logger)

    keyboardSpy.main()
