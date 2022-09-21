from dataclasses import dataclass

from exceptions import SignatureError


@dataclass
class HeaderData:
    """Датакласс для хранения данных заголовка"""
    signature = 'echo'
    filename = 'ottisk'
    int_version = 1

    hex_signature = bytes(str.encode(signature)).hex()

    version = '0001'
    algorithms = bytes(5).hex()
    size = '0100'
    hex_filename = bytes(str.encode(filename)).hex()

    header = hex_signature + version + algorithms + size + hex_filename


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

    def codefile(self, filename: str) -> None:
        """
        Функция для кодирования файла.
        :param filename: название файла
        """
        file_type = filename.split('.')[-1]
        hex_file_type = bytes(str.encode(file_type)).hex()
        result = HeaderData.header + hex_file_type + self.readfile(filename)
        self.savefile(result)

    def savefile(self, text: str) -> None:
        """
        Функция для сохранения закодированного файла.
        :param text: 16-ричный текст для записи
        """
        with open(f'{HeaderData.filename}.{HeaderData.signature}', 'wb') as output_file:
            output_file.write(bytes.fromhex(text))


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
            hex_filetype = text[len(HeaderData.header):len(HeaderData.header)+6]
            filetype = bytes.fromhex(hex_filetype).decode(encoding='utf-8')
            result = text[len(HeaderData.header) + 6:]

            self.savefile(filename, result, filetype)
        
        else:
            raise SignatureError()
