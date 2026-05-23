import math
import re


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
                    n, d = int(parts[0]), int(parts[1])
                else:
                    raise ValueError("Неправильний формат рядка дробу.")
            else:
                n, d = int(arg1), 1
        elif isinstance(arg1, int) and (isinstance(arg2, int) or arg2 is None):
            n = arg1
            d = 1 if arg2 is None else arg2
        else:
            raise TypeError("Некоректні типи аргументів для створення раціонального числа.")

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

    def __float__(self):
        return self._n / self._d

    def __getitem__(self, key):
        if key == "n": return self._n
        if key == "d": return self._d
        raise KeyError("Дозволені ключі лише 'n' або 'd'.")

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Значення має бути цілим числом.")

        if key == "n":
            n, d = value, self._d
        elif key == "d":
            if value == 0:
                raise RationalError("Знаменник не може бути змінений на нуль.")
            n, d = self._n, value
        else:
            raise KeyError("Дозволені ключі лише 'n' або 'd'.")

        g = math.gcd(n, d)
        self._n = n // g
        self._d = d // g
        if self._d < 0:
            self._n = -self._n
            self._d = -self._d

    def _convert(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other, 1)
        raise TypeError("Операція можлива лише з типом Rational або int.")

    def __add__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d + other._n * self._d, self._d * other._d)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d - other._n * self._d, self._d * other._d)

    def __rsub__(self, other):
        return Rational(other, 1).__sub__(self)

    def __mul__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._n, self._d * other._d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d, self._d * other._n)

    def __rtruediv__(self, other):
        return Rational(other, 1).__truediv__(self)



def evaluate_expression(expr_str):
    tokens = re.findall(r'\d+/\d+|\d+|[+\-*/]', expr_str.replace(" ", ""))
    parsed = []
    for t in tokens:
        if t in "+-*/":
            parsed.append(t)
        else:
            parsed.append(Rational(t))

    i = 0
    while i < len(parsed):
        if parsed[i] in ['*', '/']:
            op = parsed[i]
            left = parsed[i - 1]
            right = parsed[i + 1]
            res = left * right if op == '*' else left / right
            parsed[i - 1:i + 2] = [res]
        else:
            i += 1

    result = parsed[0]
    i = 1
    while i < len(parsed):
        op = parsed[i]
        right = parsed[i + 1]
        result = result + right if op == '+' else result - right
        i += 2

    return result


def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return

    print(f"Обробка файлу {filename}")
    for idx, line in enumerate(lines, 1):
        try:
            res_rational = evaluate_expression(line)
            res_float = float(res_rational)
            print(f"Вираз {idx}: {line}")
            print(f"  Дріб: {res_rational}")
            print(f"  Десятковий вигляд (): {res_float:.4f}\n")
        except RationalError as re_err:
            print(f"Помилка у виразі {idx} (Ділення на нуль): {re_err}\n")
        except Exception as e:
            print(f"Помилка обробки виразу {idx}: {e}\n")


if __name__ == "__main__":
    input_data = "4 - 92 - 79 * 59 * 90/16 * 75 - 55 * 82/41 * 19"
    filename = "input01.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(input_data + "\n")

    print(f"Створено файл '{filename}' з виразом.")
    process_file(filename)

    print("Демонстрація конструктора копіювання та індексів")
    orig = Rational("5/8")
    copy_version = Rational(orig)
    print(f"Оригінал: {orig}, Копія: {copy_version}")
    print(f"Чисельник через ['n']: {orig['n']}, Знаменник через ['d']: {orig['d']}")
