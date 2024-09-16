def find_max_sequence_index(n: int) -> int:
    max_sequence_index = 1
    place_value = 1
    while place_value < n:
        max_sequence_index += 1
        place_value += max_sequence_index
    return max_sequence_index


def print_n_elems(n: int, max_sequence_index: int) -> None:
    string_of_elems = ''
    for i in range(1, max_sequence_index + 1):
        string_of_elems += str(i) * i
    print(string_of_elems[:n])


if __name__ == '__main__':
    n = int(input('Введите число: '))
    max_sequence_index = find_max_sequence_index(n)
    print_n_elems(n, max_sequence_index)
