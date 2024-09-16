#  Напишите программу, которая выводит n
#  первых элементов последовательности 122333444455555…
#  (число повторяется столько раз, чему оно равно).


#  Решение построено на том свойстве этой последовательности,
#  что сумма уникальных членов последовательнсти всегда будет
#  больше либо равна индексу последнего элемента последовательности.


def find_max_sequence_index(n: int) -> int:
    """
    Определяет максимальный индекс в последовательности,
    такой что сумма всех чисел от 1 до этого индекса не превышает n.
    """
    max_sequence_index = 1
    place_value = 1

    while place_value < n:
        max_sequence_index += 1
        place_value += max_sequence_index

    return max_sequence_index


def print_n_elems(n: int, max_sequence_index: int) -> None:
    """
    Формирует строку, где каждое число повторяется согласно своему значению,
    и выводит только первые n символов этой строки.
    """
    string_of_elems = ''
    for i in range(1, max_sequence_index + 1):
        string_of_elems += str(i) * i
    print(string_of_elems[:n])


if __name__ == '__main__':
    n = int(input('Введите число: '))
    max_sequence_index = find_max_sequence_index(n)
    print_n_elems(n, max_sequence_index)
