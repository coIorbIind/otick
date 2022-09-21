import os
from typing import Tuple

from classes import Coder, Decoder
from exceptions import SignatureError


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
    print('Чтобы закодировать файл введите .......1')
    print('Чтобы декодировать файл введите .......2')
    print('-' * 40)


def main():
    coder, decoder = create_entities()
    operations = {
        '1': coder.codefile,
        '2': decoder.decode
    }

    while True:
        filename = input('Введите название файла: ')
        if os.path.exists(filename):
            break
        else:
            print('Указан несуществующий файл. Попробуйте снова')

    print_menu()
    print('Введите номер операции: ', end='')

    while True:
        operation = input()
        try:
            operations[operation](filename)
            break
        except KeyError:
            print('Указана несуществующая операция. Попробуйте снова')
        except SignatureError:
            print('Ошибка сигнатуры')


if __name__ == '__main__':
    main()
