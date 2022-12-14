import os
from typing import Tuple

from classes import Coder, Decoder
from exceptions import SignatureError, AlgorithmError


def create_entities() -> Tuple[Coder, Decoder]:
    """
    Функция для создания объектов кодера и декодера.
    :return: кортеж: coder, decoder
    """
    return Coder(), Decoder()


def print_menu() -> None:
    """
    Функция для отрисовки меню программы
    """
    print('Чтобы закодировать файл введите ..................................1')
    print('Чтобы декодировать файл введите ..................................2')
    print('Чтобы закодировать несколько файлов введите ......................3')
    print('Чтобы декодировать несколько файлов введите ......................4')
    print()
    print('Чтобы закодировать текст файла алгоритмом Шеннона-Фано введите ...5')
    print('Чтобы закодировать текст файла алгоритмом RLE введите ............6')
    print('-' * 67)


def main():
    coder, decoder = create_entities()
    operations = {
        '1': coder.code_file,
        '2': decoder.decode,
        '3': coder.code_files,
        '4': decoder.decode_files,
        '5': coder.shennon_fano_code,
        '6': coder.rle_code,
    }
    print_menu()
    print('Введите номер операции: ', end='')

    while True:
        operation = input()
        if operation not in operations:
            print('Указана несуществующая операция. Попробуйте снова')
        else:
            break

    while True:
        if operation in ['1', '2', '4', '5', '6']:
            data = input('Введите название файла: ')
            if os.path.exists(data):
                break
            else:
                print('Указан несуществующий файл. Попробуйте снова')
        elif operation in ['3']:
            data = input('Введите название файлов: ').split()
            for filename in data:
                if not filename:
                    print('Указан несуществующий файл. Попробуйте снова')
            else:
                break

    try:
        operations[operation](data)
    except SignatureError:
        print('Ошибка сигнатуры')

    except AlgorithmError:
        print('Ошибка кода алгоритма')


if __name__ == '__main__':
    main()
