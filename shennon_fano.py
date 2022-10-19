from collections import defaultdict
from typing import Optional


class ShennonFano:
    def __init__(self):
        self.result = defaultdict(str)

    def count_frequencies(self, text: str) -> dict:
        frequencies = defaultdict(int)
        for char in text:
            frequencies[char] += 1
        frequencies = dict(sorted(frequencies.items(), key=lambda x: (-x[1], text.find(x[0]))))
        return frequencies

    def separate(self, frequencies: dict) -> Optional[tuple]:
        if len(frequencies) == 0:
            return

        first_dict = dict()
        total_frequency = sum(frequencies.values())
        char = list(frequencies.keys())[0]
        temp_frequency = frequencies[char]
        first_dict[char] = temp_frequency
        frequencies.pop(char)

        for char, frequency in frequencies.items():
            if temp_frequency + frequency > total_frequency // 2:
                break
            temp_frequency += frequency
            first_dict[char] = frequency

        for char in first_dict:
            if char in frequencies:
                frequencies.pop(char)
            self.result[char] += '0'

        for char in frequencies:
            self.result[char] += '1'

        return first_dict, frequencies

    def coding(self, frequencies):
        first, second = self.separate(frequencies)
        if len(first) != 1:
            self.coding(first)
        if len(second) != 1:
            self.coding(second)
