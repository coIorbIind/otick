from dataclasses import dataclass
from typing import List

from exceptions import SignatureError


@dataclass
class HeaderData:
    """Датакласс для хранения данных заголовка"""
    signature = 'echo'
    filename = 'ottisk'
    archive_filename = 'archive'
    int_version = 1

    hex_signature = bytes(str.encode(signature)).hex()

    version = '0001'
    algorithms = bytes(5).hex()
    hex_filename = bytes(str.encode(filename)).hex()

    header = hex_signature + version + algorithms + hex_filename


class Coder:
    """Класс кодера"""
    def readfile(self, filename: str) -> str:
        """
        Функция для считывая файла.
        :param filename: название файла.
        :return: содержание файла в 16-ричной системе
        """
        with open(filename, 'rb') as input_file:
            text = input_file.read().hex()
            return text

    def code_file(self, filename: str) -> None:
        """
        Функция для кодирования файла.
        :param filename: название файла
        """
        file_type = filename.split('.')[-1]
        hex_file_type = bytes(str.encode(file_type)).hex()
        file_data = self.readfile(filename)
        file_size = format(len(file_data) // 2, 'x')
        hex_file_size = '0' * (6 - len(file_size)) + file_size
        result = HeaderData.header + hex_file_size + hex_file_type + file_data
        self.savefile(result)

    def savefile(self, text: str, many: bool = False) -> None:
        """
        Функция для сохранения закодированного файла.
        :param text: 16-ричный текст для записи,
        :param many: True - создается архив для нескольких файлов
        """
        if many:
            with open(f'{HeaderData.archive_filename}.{HeaderData.signature}', 'wb') as output_file:
                output_file.write(bytes.fromhex(text))
        else:
            with open(f'{HeaderData.filename}.{HeaderData.signature}', 'wb') as output_file:
                output_file.write(bytes.fromhex(text))

    def code_files(self, filenames: List[str]) -> None:
        """
        Функция для кодирования нескольких файлов.
        :param filenames: название файлов
        """
        result = HeaderData.header
        for filename in filenames:
            file_type = filename.split('.')[-1]
            hex_file_type = bytes(str.encode(file_type)).hex()
            file_data = self.readfile(filename)
            file_size = format(len(file_data) // 2, 'x')
            hex_file_size = '0' * (6 - len(file_size)) + file_size
            result += hex_file_size + hex_file_type + file_data

        self.savefile(result, many=True)


class Decoder:
    """Класс декодера"""
    def readfile(self, filename: str) -> str:
        """
        Функция для считывая файла.
        :param filename: название файла.
        :return: содержание файла в 16-ричной системе
        """
        with open(filename, 'rb') as input_file:
            text = input_file.read().hex()

            return text

    def savefile(self, filename: str, text: str, filetype: str) -> None:
        """
        Функция для сохранения декодированного файла.
        :param filename: название исходного файла.
        :param text: 16-ричный текст для записи.
        :param filetype: расширение исходного файла
        """
        with open(f"{filename.split('.')[0]}.{filetype}", 'wb') as output_file:
            output_file.write(bytes.fromhex(text))

    def decode(self, filename: str) -> None:
        """
        Функция для декодироваия файла.
        :param filename: название файла
        """
        text = self.readfile(filename)
        if text.startswith(HeaderData.hex_signature):
            hex_filetype = text[len(HeaderData.header) + 6:len(HeaderData.header)+12]
            filetype = bytes.fromhex(hex_filetype).decode(encoding='utf-8')
            result = text[len(HeaderData.header) + 12:]

            self.savefile(filename, result, filetype)
        
        else:
            raise SignatureError()

    def decode_files(self, filename: str) -> None:
        """
        Функция для декодироваия файла.
        :param filename: название файла
        """
        text = self.readfile(filename)
        if text.startswith(HeaderData.hex_signature):
            ptr = len(HeaderData.header)
            data = text[ptr:]
            ind = 1
            while data:
                file_size = int(text[ptr:ptr + 6],  16) * 2
                hex_filetype = text[ptr + 6:ptr + 12]
                filetype = bytes.fromhex(hex_filetype).decode(encoding='utf-8')
                result = text[ptr + 12: ptr + 12 + file_size]
                self.savefile(f'file{ind}', result, filetype)

                ptr = ptr + 12 + file_size
                data = text[ptr:]
                ind += 1

        else:
            raise SignatureError()
