import math


def calculate_sequence_element(x, k):
    numerator = x ** k
    denominator = math.factorial(k + 1) * math.factorial(k)
    return numerator / denominator


def calculate_product(n):
    p = 1.0
    for k in range(1, n + 1):
        p *= (2 + 1 / (k ** 2))
    return p


def calculate_matrix_determinant(a, n):
    if n == 1: return a
    if n == 2: return a ** 2 - 1
    d_prev2, d_prev1 = a, a ** 2 - 1
    for _ in range(3, n + 1):
        d_current = a * d_prev1 - d_prev2
        d_prev2, d_prev1 = d_prev1, d_current
    return d_prev1


def calculate_recurrent_sum(n):
    if n == 1: return 1.0
    if n == 2: return 2.0
    a_prev2, a_prev1 = 1.0, 1.0
    total_sum = 2.0
    for k in range(3, n + 1):
        a_current = a_prev1 + (a_prev2 / k)
        total_sum += a_current
        a_prev2, a_prev1 = a_prev1, a_current
    return total_sum


def taylor_series_ln(x, eps):
    total_sum = 0.0
    k = 1
    term = x
    while abs(term) > eps:
        total_sum += term
        k += 1
        term = ((-1) ** (k - 1)) * (x ** k) / k
    return total_sum

if __name__ == "__main__":
    print("Результати обчислень")
    print("a) Елемент послідовності (x=2, k=3):", calculate_sequence_element(x=2, k=3))
    print("b) Добуток параметру (n=5):", calculate_product(n=5))
    print("c) Визначник матриці (a=3, n=4):", calculate_matrix_determinant(a=3, n=4))
    print("d) Рекурентна сума (n=5):", calculate_recurrent_sum(n=5))
    x_val, epsilon = 0.5, 1e-6
    t_res = taylor_series_ln(x_val, epsilon)
    m_res = math.log(1 + x_val)
    print("e) Ряд Тейлора для ln(1+x):")
    print(f"   Результат Тейлора:  {t_res}")
    print(f"   Результат math.log: {m_res}")
    print(f"   Різниця:            {abs(t_res - m_res)}")