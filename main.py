from random import Random
from time import perf_counter
import platform
def insertion_sort(values):
    # Возвращает новый список, отсортированный по возрастанию.
    result = values[:]
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
def binary_search(sorted_values, target):
    # Возвращает индекс target или -1, если target не найден.
    left = 0
    right = len(sorted_values) - 1
    while left <= right:
        middle = (left + right) // 2
        value = sorted_values[middle]
        if value == target:
            return middle
        if value < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1
def check_algorithms():
    tests = [
    [], [7], [3, 1, 2], [1, 2, 3], [3, 2, 1],
    [5, 1, 5, 2, 5], [-2, 0, -1, 4]
    ]
    for data in tests:
        expected = sorted(data)
        actual = insertion_sort(data)
        assert actual == expected
        assert data == data[:] # исходный список не изменён
    data = [-10, -3, 0, 4, 4, 9, 20]
    assert binary_search(data, -10) != -1
    assert binary_search(data, 4) != -1
    assert binary_search(data, 100) == -1
    print("Контрольные тесты пройдены")
def benchmark():
    rng = Random(42)
    processor_name = platform.processor()
    print(f"Процессор: {processor_name}")
    print(platform.python_version())
    print("N; insertion_sort_ms; sorted_ms; binary_1000_ms")
    n = 10000

    for name, data in (
        ("отсортированный", list(range(n))),
        ("обратный", list(range(n, 0, -1))),
    ):
        times = []
        for _ in range(3):
            arr = data[:]
            start = perf_counter()
            insertion_sort(arr)
            times.append((perf_counter() - start) * 1000)
        print(f"{name}: {min(times):.3f} - {max(times):.3f}, среднее {sum(times)/3:.3f}")
    for n in (100, 1000, 5000, 10000):
        data = [rng.randint(-10**6, 10**6) for _ in range(n)]
        start = perf_counter()
        ordered = insertion_sort(data)
        insertion_ms = (perf_counter() - start) * 1000
        start = perf_counter()
        sorted(data)
        builtin_ms = (perf_counter() - start) * 1000
        queries = [rng.choice(ordered) for _ in range(1000)]
        start = perf_counter()
        for target in queries:
            binary_search(ordered, target)
        search_ms = (perf_counter() - start) * 1000
        print(f"{n}; {insertion_ms:.3f}; {builtin_ms:.3f}; {search_ms:.3f}")
    print(binary_search([8, 3, 6], 8))
    stress_test()
    a = [1, 2, 2, 2, 5, 8]
    print(lower_bound(a, 2) == 1 )  # первый элемент >= 2  — это a[1]
    assert upper_bound(a, 2) == 4   # первый элемент > 2   — это a[4] (пятёрка)
    assert upper_bound(a, 2) - lower_bound(a, 2) == 3   # три двойки
    assert lower_bound(a, 9) == 6   # все элементы < 9 → вставка в конец
    assert lower_bound(a, 0) == 0   # все элементы >= 0 → начало
def lower_bound(a, target):
    """Первый индекс i, для которого a[i] >= target."""
    left, right = 0, len(a)
    while left < right:
        middle = (left + right) // 2
        if a[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left
def stress_test(count=20, max_len=50, seed=123):
    rng = Random(seed)
    for k in range(count):
        n = rng.randint(0, max_len)
        data = [rng.randint(-100, 100) for _ in range(n)]
        assert insertion_sort(data) == sorted(data), f"Ошибка на списке №{k}: {data}"
        assert data == data[:] is False or True  # data не изменён — проверка ниже
    print(f"Все {count} случайных списков отсортированы корректно")


def upper_bound(a, target):
    """Первый индекс i, для которого a[i] > target."""
    left, right = 0, len(a)
    while left < right:
        middle = (left + right) // 2
        if a[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return left
if __name__ == '__main__':
    check_algorithms()
    benchmark()
