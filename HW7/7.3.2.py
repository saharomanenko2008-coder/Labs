import math


class RationalValueError(ValueError):
    def __init__(self, message="Некоректний тип операнда для арифметичної операції."):
        super().__init__(message)


class RationalError(ZeroDivisionError):
    def __init__(self, message="Знаменник не може дорівнювати нулю."):
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
                n, d = int(parts[0]), int(parts[1])
            else:
                n, d = int(arg1), 1
        elif isinstance(arg1, int) and (isinstance(arg2, int) or arg2 is None):
            n = arg1
            d = 1 if arg2 is None else arg2
        else:
            raise RationalValueError("Конструктор Rational приймає лише цілі числа, рядки 'n/d' або інший Rational.")

        if d == 0:
            raise RationalError()

        g = math.gcd(n, d)
        self._n = n // g
        self._d = d // g
        if self._d < 0:
            self._n = -self._n
            self._d = -self._d

    def __str__(self):
        return f"{self._n}/{self._d}" if self._d != 1 else f"{self._n}"

    def _convert(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Rational(other, 1)

        raise RationalValueError(
            f"Арифметична операція не має сенсу для типів Rational та {type(other).__name__}. "
            f"Дозволено лише Rational або int."
        )

    def __add__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d + other._n * self._d, self._d * other._d)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d - other._n * self._d, self._d * other._d)

    def __rsub__(self, other):
        return Rational(other).__sub__(self)

    def __mul__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._n, self._d * other._d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._convert(other)
        return Rational(self._n * other._d, self._d * other._n)

    def __rtruediv__(self, other):
        return Rational(other).__truediv__(self)



if __name__ == "__main__":
    a = Rational("3/4")
    b = Rational(2, 3)

    print(f"Успішні операції:")
    print(f"  {a} + {b} = {a + b}")
    print(f"  {a} * 5 = {a * 5}")
    print("-" * 50)

    invalid_operands = [2.5, "hello", [1, 2]]

    print("Тестування виключення RationalValueError:")
    for bad_operand in invalid_operands:
        try:
            print(f"Спроба виконати: {a} + {bad_operand}")
            result = a + bad_operand
        except RationalValueError as e:
            print(f"Перехоплено виключення: {e}\n")
