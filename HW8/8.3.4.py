import math


def calculate_alternating_sequence(x, k):
    numerator = ((-1) ** k) * (x ** k)
    denominator = math.factorial(k ** 2 + k)
    return numerator / denominator


def calculate_fraction_product(n):
    if n < 2: return 1.0
    p = 1.0
    for i in range(2, n + 1):
        p *= (1 - 1 / (i ** 2))
    return p


def calculate_band_matrix_determinant(n):
    if n <= 0: return 0
    if n == 1: return 1
    if n == 2: return -2

    d_prev2 = 1
    d_prev1 = -2

    for _ in range(3, n + 1):
        d_current = 5 * d_prev1 - 6 * d_prev2
        d_prev2, d_prev1 = d_prev1, d_current
    return d_prev1

def calculate_factorial_recurrent_sum(n):
    if n <= 0: return 0.0
    if n == 1: return 0.0
    if n == 2: return 2.0

    a_prev2 = 0.0
    a_prev1 = 1.0
    total_sum = 2.0

    for k in range(3, n + 1):
        a_current = a_prev1 + (a_prev2 / math.factorial(k - 1))
        total_sum += math.factorial(k) * a_current
        a_prev2, a_prev1 = a_prev1, a_current
    return total_sum

def taylor_series_fraction(x, eps):
    total_sum = 0.0
    k = 0
    term = 1.0
    while abs(term) > eps:
        total_sum += term
        k += 1
        term = ((-1) ** k) * (x ** k)
    return total_sum

if __name__ == "__main__":
    print("Результати обчислень")
    print("a) Елемент послідовності (x=2, k=2):", calculate_alternating_sequence(x=2, k=2))
    print("b) Добуток проміжків P_n (n=4):", calculate_fraction_product(n=4))
    print("c) Визначник матриці (n=4):", calculate_band_matrix_determinant(n=4))
    print("d) Сума послідовності S_n (n=4):", calculate_factorial_recurrent_sum(n=4))
    x_val, epsilon = 0.4, 1e-6
    t_res = taylor_series_fraction(x_val, epsilon)
    m_res = 1 / (1 + x_val)
    print("e) Ряд Тейлора для 1 / (1 + x):")
    print(f"   Результат Тейлора:  {t_res}")
    print(f"   Результат math-формули: {m_res}")
    print(f"   Різниця:            {abs(t_res - m_res)}")
