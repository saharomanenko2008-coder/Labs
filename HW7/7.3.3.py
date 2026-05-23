import math
import os

class RationalValueError(ValueError):
    def __init__(self, message="Некоректний тип даних для раціонального числа або списку."):
        super().__init__(message)


class RationalError(ZeroDivisionError):
    def __init__(self, message="Знаменник раціонального числа не може дорівнювати нулю."):
        super().__init__(message)


class Rational:
    def __init__(self, arg1, arg2=None):
        if isinstance(arg1, Rational):
            self._n = arg1._n
            self._d = arg1._d
            return

        if isinstance(arg1, str) and arg2 is None:
            if '/' in arg1:
                parts = arg1.split('/')
                if len(parts) == 2:
                    try:
                        n, d = int(parts[0]), int(parts[1])
                    except ValueError:
                        raise RationalValueError(f"Некоректні символи у дробі '{arg1}'.")
                else:
                    raise RationalValueError(f"Неправильний формат рядка дробу '{arg1}'.")
            else:
                try:
                    n, d = int(arg1), 1
                except ValueError:
                    raise RationalValueError(f"Рядок '{arg1}' не є цілим числом.")
        elif isinstance(arg1, int) and not isinstance(arg1, bool) and (isinstance(arg2, int) or arg2 is None):
            n = arg1
            d = 1 if arg2 is None else arg2
        else:
            raise RationalValueError("Rational приймає лише цілі числа, рядки 'n/d' або інший Rational.")

        if d == 0:
            raise RationalError(f"Спроба створення дробу {n}/{d} з нульовим знаменником.")

        g = math.gcd(n, d)
        self._n = n // g
        self._d = d // g
        if self._d < 0:
            self._n = -self._n
            self._d = -self._d

    def __str__(self):
        return f"{self._n}/{self._d}" if self._d != 1 else f"{self._n}"

    def _convert(self, other):
        if isinstance(other, Rational): return other
        if isinstance(other, int) and not isinstance(other, bool): return Rational(other, 1)
        raise RationalValueError(f"Операція не підтримується для типу {type(other).__name__}.")

    def __add__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d + other._n * self._d, self._d * other._d)


class RationalList:
    def __init__(self, initial_data=None):
        self._items = []
        if initial_data is not None:
            if isinstance(initial_data, RationalList):
                self._items = [Rational(item) for item in initial_data._items]
            elif isinstance(initial_data, list):
                for element in initial_data:
                    self._validate_and_append(element)
            else:
                self._validate_and_append(initial_data)

    def _validate_and_append(self, element):
        if isinstance(element, Rational):
            self._items.append(Rational(element))  # Копіюємо об'єкт
        elif isinstance(element, int) and not isinstance(element, bool):
            self._items.append(Rational(element, 1))
        else:
            raise RationalValueError(
                f"Спроба додавання некоректних даних типу '{type(element).__name__}' до RationalList. "
                f"Дозволено лише Rational або int."
            )

    def __str__(self):
        elements_str = ", ".join(str(x) for x in self._items)
        return f"RationalList(size={len(self)}, elements=[{elements_str}])"

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self._items[index] = Rational(value)
        elif isinstance(value, int) and not isinstance(value, bool):
            self._items[index] = Rational(value, 1)
        else:
            raise RationalValueError(f"Некоректний тип '{type(value).__name__}' для запису за індексом.")

    def __len__(self):
        return len(self._items)

    def __add__(self, other):
        new_list = RationalList(self)
        if isinstance(other, RationalList):
            for item in other._items:
                new_list._items.append(Rational(item))
        else:
            new_list._validate_and_append(other)
        return new_list

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            for item in other._items:
                self._items.append(Rational(item))
        else:
            self._validate_and_append(other)
        return self

    def sum_all(self):
        result = Rational(0, 1)
        for item in self._items:
            result = result + item
        return result


def process_input_file(filename):
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не знайдено.")
        return

    rational_list = RationalList()
    print(f"\nОбробка файлу: {filename} ")

    with open(filename, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            tokens = line.strip().split()
            for token in tokens:
                try:
                    num = Rational(token)
                    rational_list += num
                except RationalValueError as e:
                    print(f"[Рядок {line_num}] Помилка валідації для '{token}': {e}")
                except RationalError as e:
                    print(f"[Рядок {line_num}] Критична помилка математики для '{token}': {e}")

    print(f"  Завантажено елементів: {len(rational_list)}")
    print(f"  Вміст списку: {rational_list}")
    print(f"  СУМА ПОСЛІДОВНОСТІ: {rational_list.sum_all()}")


if __name__ == "__main__":
    test_data = {
        "input01.txt": "4 12/3 5/2\n-1/2 8 0",
        "input02.txt": "1/3   2/3   3/3\n4/3   5/3",
        "input03.txt": "5 10/2 hello 7/0 3.14"
    }

    for name, content in test_data.items():
        with open(name, "w", encoding="utf-8") as f:
            f.write(content)

    for filename in ["input01.txt", "input02.txt", "input03.txt"]:
        process_input_file(filename)

    print("\n" + "="*60)
    print("Ручна демонстрація RationalValueError для RationalList:")
    try:
        r_list = RationalList([Rational(1, 2), 5])
        print(f"Початковий список: {r_list}")
        print("Спроба виконати: r_list += 4.56 (тип float)")
        r_list += 4.56
    except RationalValueError as err:
        print(f"Перехоплено виключення в коді програми: {err}")
