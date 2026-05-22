import re


class CustomSetIterator:
    def __init__(self, elements):
        self._elements = list(elements)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._elements):
            result = self._elements[self._index]
            self._index += 1
            return result
        raise StopIteration


class CustomSet:
    def __init__(self, initial_data=None):
        self._data = set()
        if initial_data is not None:
            if isinstance(initial_data, CustomSet):
                # Конструктор копіювання
                self._data = set(initial_data._data)
            elif isinstance(initial_data, (list, tuple, set)):
                self._data = set(initial_data)
            else:
                self._data.add(initial_data)

    def __iter__(self):
        return CustomSetIterator(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        elements_str = ", ".join(f"'{x}'" if isinstance(x, str) else str(x) for x in self)
        return f"CustomSet(size={len(self)}, elements={{{elements_str}}})"

    def _convert_operand(self, other):
        if isinstance(other, CustomSet):
            return other
        return CustomSet(other)

    def __mul__(self, other):
        other_set = self._convert_operand(other)
        return CustomSet(self._data.intersection(other_set._data))

    def __add__(self, other):
        other_set = self._convert_operand(other)
        return CustomSet(self._data.union(other_set._data))

    def __sub__(self, other):
        other_set = self._convert_operand(other)
        return CustomSet(self._data.difference(other_set._data))

    def __truediv__(self, other):
        other_set = self._convert_operand(other)
        return CustomSet(self._data.symmetric_difference(other_set._data))


def get_words_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read().lower()
            words = re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄґҐ\']+\b', text)
            return CustomSet(words)
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
        return CustomSet()


def print_set_via_iterator(title, custom_set):
    print(f"\n🔹 {title} (Всього: {len(custom_set)}):")
    if len(custom_set) == 0:
        print("   [Множина порожня]")
        return
    print("   Елементи: ", end="")
    for item in custom_set:
        print(f"[{item}]", end=" ")
    print()


if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]

    with open("file1.txt", "w", encoding="utf-8") as f:
        f.write("яблуко груша банани слива")
    with open("file2.txt", "w", encoding="utf-8") as f:
        f.write("груша банани виноград ківі")
    with open("file3.txt", "w", encoding="utf-8") as f:
        f.write("банани груша ананас")

    print("--- Завантаження слів із файлів ---")
    set1 = get_words_from_file(files[0])
    set2 = get_words_from_file(files[1])
    set3 = get_words_from_file(files[2])

    print(f"Файл 1: {set1}")
    print(f"Файл 2: {set2}")
    print(f"Файл 3: {set3}")
    print("=" * 60)

    words_in_all = set1 * set2 * set3
    print_set_via_iterator("Слова, які є у ВСІХ файлах", words_in_all)

    words_at_least_one = set1 + set2 + set3
    print_set_via_iterator("Слова, які є ПРИНАЙМНІ в одному файлі", words_at_least_one)

    words_only_in_first = set1 - set2 - set3
    print_set_via_iterator("Слова, які є ЛИШЕ у першому файлі", words_only_in_first)

    print("\n" + "=" * 60)
    print("Демонстрація операцій з окремим словом (як одноелементна множина):")
    test_op = words_in_all - "банани"
    print(f"   Перетин без слова 'банани': {test_op}")
