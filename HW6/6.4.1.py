class CustomListIterator:
    def __init__(self, data_list):
        odds = sorted([x for x in data_list if x % 2 != 0])
        evens = sorted([x for x in data_list if x % 2 == 0], reverse=True)

        self._iterable_data = odds + evens
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._iterable_data):
            result = self._iterable_data[self._index]
            self._index += 1
            return result
        raise StopIteration


class CustomList:
    def __init__(self, initial_data=None):
        """Конструктор з підтримкою копіювання."""
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
            raise TypeError("CustomList може містити лише цілі числа.")
        self._data.append(item)

    def __str__(self):
        return f"CustomList(elements={self._data})"

    def __iter__(self):
        return CustomListIterator(self._data)

def print_numbers_from_file(filename):
    import re
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
        return

    str_numbers = re.findall(r'\b[-+]?\d+\b', text)
    int_numbers = [int(num) for num in str_numbers]

    custom_list = CustomList(int_numbers)

    print("--- Початковий вміст файлу (знайдені числа) ---")
    print(custom_list)
    print("-" * 45)

    print("--- Виведення елементів за допомогою нового ітератора ---")
    print("Правило: спочатку непарні (зростання), потім парні (спадання):")

    for number in custom_list:
        print(number, end=" ")
    print("\n" + "-" * 45)


if __name__ == "__main__":
    file_content = "10 5 3 8 2 1 7 4 6 9"
    test_filename = "numbers_task.txt"

    with open(test_filename, "w", encoding="utf-8") as f:
        f.write(file_content)

    print(f"Створено файл '{test_filename}' із числами: {file_content}\n")

    print_numbers_from_file(test_filename)
