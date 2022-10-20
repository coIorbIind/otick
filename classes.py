from dataclasses import dataclass
from typing import List
from collections import defaultdict
import json
from string import digits

from exceptions import SignatureError, AlgorithmError
from shennon_fano import ShennonFano


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

    @staticmethod
    def recalculate_header():
        HeaderData.header = HeaderData.hex_signature + HeaderData.version + HeaderData.algorithms + HeaderData.hex_filename


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

    def shennon_fano_code(self, filename: str) -> None:
        """
        Функция для кодирования текста файла алгоритмом Шеннона-Фано.
        :param filename: название файла
        """
        HeaderData.algorithms = '0000000001'
        HeaderData.version = '0010'
        HeaderData.recalculate_header()
        file_type = filename.split('.')[-1]
        hex_file_type = bytes(str.encode(file_type)).hex()
        with open(filename, encoding='utf8') as file:
            data = file.read()

        shennon_coder = ShennonFano()
        frequencies = shennon_coder.count_frequencies(data)
        shennon_coder.coding(frequencies)
        # for char, code in shennon_coder.result.items():
        #     print(f'{char}: {code}')

        hex_codes = bytes(str.encode(json.dumps(shennon_coder.result))).hex()

        text = ''
        for char in data:
            text += shennon_coder.result[char]

        file_size = format(len(text), 'x')
        hex_file_size = '0' * (6 - len(file_size)) + file_size
        result = HeaderData.header + hex_file_size + hex_file_type + hex_codes + text
        self.savefile(result)

    def rle_code(self, filename: str) -> None:
        """
        Функция для кодирования текста файла алгоритмом RLE.
        :param filename: название файла
        """
        HeaderData.algorithms = '0000000010'
        HeaderData.version = '0010'
        HeaderData.recalculate_header()
        file_type = filename.split('.')[-1]
        hex_file_type = bytes(str.encode(file_type)).hex()
        with open(filename, encoding='utf8') as file:
            data = file.read()

        text = ''
        ptr = 0
        temp_count = 0
        previous_char = ''
        while ptr != len(data):
            current_char = data[ptr]
            if current_char == previous_char:
                temp_count += 1
            elif temp_count == 0:
                temp_count = 1
            else:
                text += f'{temp_count}{previous_char}'
                temp_count = 1
            previous_char = current_char
            ptr += 1
        text += f'{temp_count}{previous_char}'
        print(text)
        hex_text = bytes(str.encode(text)).hex()
        print(hex_text)
        file_size = format(len(text), 'x')
        hex_file_size = '0' * (6 - len(file_size)) + file_size
        result = HeaderData.header + hex_file_size + hex_file_type + hex_text
        self.savefile(result)

        # frequencies = count_frequencies(data)
        # p = list(frequencies.keys())[-1]
        # text = ''
        # ptr = 0
        # temp_count = 0
        # previous_char = ''
        # while ptr != len(data):
        #     current_char = data[ptr]
        #     if current_char == previous_char:
        #         temp_count += 1
        #     else:
        #         if temp_count >= 4 or previous_char == p:
        #             text += f'{p}{temp_count}{previous_char}'
        #         else:
        #             text += previous_char * temp_count
        #         temp_count = 1
        #     previous_char = current_char
        #     ptr += 1
        # if temp_count >= 4 or previous_char == p:
        #     text += f'{p}{temp_count}{previous_char}'
        # else:
        #     text += previous_char * temp_count
        # hex_text = bytes(str.encode(text)).hex()
        # file_size = format(len(text), 'x')
        # hex_file_size = '0' * (6 - len(file_size)) + file_size
        # result = HeaderData.header + hex_file_size + hex_file_type + hex_text
        # self.savefile(result)


def count_frequencies(text: str) -> dict:
    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1
    frequencies = dict(sorted(frequencies.items(), key=lambda x: (-x[1], text.find(x[0]))))
    return frequencies


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
        Функция для запуска подходящей декодировки файла.
        :param filename: название файла
        """
        text = self.readfile(filename)
        if text.startswith(HeaderData.hex_signature):
            hex_filetype = text[len(HeaderData.header) + 6:len(HeaderData.header) + 12]
            algorithms = text[len(HeaderData.hex_signature + HeaderData.version):
                              len(HeaderData.hex_signature + HeaderData.version) + 10]
            filetype = bytes.fromhex(hex_filetype).decode(encoding='utf-8')

            if algorithms == '0' * 10:
                result = text[len(HeaderData.header) + 12:]

            elif algorithms == '0' * 9 + '1':
                result = bytes(str.encode(self.shennon_fano_decode(text))).hex()

            elif algorithms == '0000000010':
                text = text[len(HeaderData.header) + 12:]
                text = bytes.fromhex(text).decode(encoding='utf-8')
                result = bytes(str.encode(self.rle_decode(text))).hex()

            else:
                raise AlgorithmError()

            self.savefile(filename, result, filetype)
        else:
            raise SignatureError()

    def rle_decode(self, data: str) -> str:
        frequencies = count_frequencies(data)
        if not frequencies:
            return ''
        # p = list(frequencies.keys())[0]
        text = ''
        ptr = 0
        temp_digits = ''
        current_char = ''
        while ptr != len(data):
            current_char = data[ptr]
            if current_char in digits:
                temp_digits += current_char
            else:
                text += current_char * int(temp_digits)
                temp_digits = ''
            ptr += 1
        return text
            # if current_char == p:
            #     if temp_chars != '':
            #         num = temp_chars[:-1] * int(temp_chars[:-1])
            #     temp_chars = ''



    def shennon_fano_decode(self, text: str) -> str:
        file_size = int(text[len(HeaderData.header):len(HeaderData.header) + 6], 16)
        str_dict = text[len(HeaderData.header) + 12:-file_size]
        dct = json.loads(bytes.fromhex(str_dict).decode(encoding='utf-8'))
        inv_dct = {value: key for key, value in dct.items()}
        file_data = text[-file_size:]
        ptr = 0
        code = ''
        text = ''
        while ptr != len(file_data):
            code += file_data[ptr]
            char = inv_dct.get(code)
            if char is not None:
                text += char
                code = ''
            ptr += 1

        return text

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
                file_size = int(text[ptr:ptr + 6], 16) * 2
                hex_filetype = text[ptr + 6:ptr + 12]
                filetype = bytes.fromhex(hex_filetype).decode(encoding='utf-8')
                result = text[ptr + 12: ptr + 12 + file_size]
                self.savefile(f'file{ind}', result, filetype)

                ptr = ptr + 12 + file_size
                data = text[ptr:]
                ind += 1

        else:
            raise SignatureError()
