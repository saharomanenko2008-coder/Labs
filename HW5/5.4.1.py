import re

class CustomList:
    def __init__(self, initial_data=None):
        self._data = []
        if initial_data is not None:
            if isinstance(initial_data, CustomList):
                self._data = list(initial_data._data)
            elif isinstance(initial_data, (list, tuple)):
                for item in initial_data:
                    self._validate_and_append(item)
            else:
                self._validate_and_append(initial_data)

    def _validate_and_append(self, item):
        if not isinstance(item, int) or isinstance(item, bool):
            raise TypeError("CustomList може містити лише цілі числа (int).")
        self._data.append(item)

    def __str__(self):
        return f"CustomList(size={len(self._data)}, elements={self._data})"

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Значення має бути цілим числом.")
        self._data[index] = value

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        return item in self._data

    def __iadd__(self, other):
        if isinstance(other, CustomList):
            self._data.extend(other._data)
        elif isinstance(other, int) and not isinstance(other, bool):
            self._data.append(other)
        else:
            raise TypeError("Правий операнд має бути типу CustomList або int.")
        return self

    def __isub__(self, other):
        if isinstance(other, CustomList):
            to_remove = other._data
        elif isinstance(other, int) and not isinstance(other, bool):
            to_remove = [other]
        else:
            raise TypeError("Правий операнд має бути типу CustomList або int.")

        self._data = [item for item in self._data if item not in to_remove]
        return self

    def __imul__(self, other):
        if not isinstance(other, int) or isinstance(other, bool):
            raise TypeError("Правий операнд для *= має бути цілим числом.")
        if other < 0:
            raise ValueError("Множник не може бути від'ємним.")
        self._data *= other
        return self

    def sum(self):
        return sum(self._data)


def process_text_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
        return

    str_numbers = re.findall(r'\b[-+]?\d+\b', text)
    int_numbers = [int(num) for num in str_numbers]

    numbers_list = CustomList(int_numbers)
    print("--- Завантажені дані з файлу ---")
    print(numbers_list)
    print("-" * 32)

    total_sum = numbers_list.sum()
    total_count = len(numbers_list)
    print(f"Загальна кількість чисел у тексті: {total_count}")
    print(f"Сума всіх чисел у тексті: {total_sum}")

    target_numbers = [1, 3, 1984, 7777]
    found_any = any(num in numbers_list for num in target_numbers)
    print(f"Чи трапляється бодай одне з чисел {target_numbers}?: {'Так' if found_any else 'Ні'}")

    non_zero_list = CustomList(numbers_list)
    non_zero_list -= 0

    print(f"Кількість чисел відмінних від нуля: {len(non_zero_list)}")


if __name__ == "__main__":
    sample_text = """
    У 1984 році відбулися важливі події. Всього було 3 спроби.
    Рахунок склав 0:0, а потім змінився на 1. Помилка -5 була критичною.
    Тест завершено з кодом 0.
    """

    input_filename = "input_text.txt"
    with open(input_filename, "w", encoding="utf-8") as f:
        f.write(sample_text)

    print(f"Створено тестовий файл '{input_filename}' з таким вмістом:\n{sample_text}")

    process_text_file(input_filename)
