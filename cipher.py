import os
import base64
import time
import matplotlib.pyplot as plt
from typing import Callable, List, Dict
from functools import reduce
from exceptions import *


class Cipher:
    def __init__(self, key: str):
        if not key or not isinstance(key, str):
            raise InvalidKeyError("Klucz musi być niepustym ciągiem znaków")
        self.key = key
        self.encryption_times = []
        self.decryption_times = []

    def encrypt(self, text: str) -> str:
        """Szyfruje tekst przy użyciu klucza"""
        start_time = time.time()
        result = self._encrypt(text)
        end_time = time.time()
        self.encryption_times.append(end_time - start_time)
        return result

    def _encrypt(self, text: str) -> str:
        raise NotImplementedError("Metoda _encrypt musi być zaimplementowana w klasie pochodnej")

    def decrypt(self, encrypted_text: str) -> str:
        """Deszyfruje tekst przy użyciu klucza"""
        start_time = time.time()
        result = self._decrypt(encrypted_text)
        end_time = time.time()
        self.decryption_times.append(end_time - start_time)
        return result

    def _decrypt(self, encrypted_text: str) -> str:
        raise NotImplementedError("Metoda _decrypt musi być zaimplementowana w klasie pochodnej")

    def save_to_file(self, filename: str, text: str) -> None:
        """Zapisuje tekst do pliku"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
        except (IOError, OSError) as e:
            raise FileOperationError(f"Błąd podczas zapisu do pliku: {e}")

    def read_from_file(self, filename: str) -> str:
        """Odczytuje tekst z pliku"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except (IOError, OSError) as e:
            raise FileOperationError(f"Błąd podczas odczytu z pliku: {e}")

    @staticmethod
    def apply_lambda_operation(text: str, operation: Callable[[str], str]) -> str:
        """Stosuje operację lambda na tekście"""
        return operation(text)

    @staticmethod
    def filter_text(text: str, condition: Callable[[str], bool]) -> str:
        """Filtruje tekst używając funkcji filter"""
        return ''.join(filter(condition, text))

    @staticmethod
    def map_text(text: str, transformation: Callable[[str], str]) -> str:
        """Transformuje tekst używając funkcji map"""
        return ''.join(map(transformation, text))

    def get_performance_stats(self) -> Dict[str, float]:
        """Zwraca statystyki czasu wykonania"""
        if not self.encryption_times or not self.decryption_times:
            return {}

        stats = {
            'avg_encrypt': reduce(lambda x, y: x + y, self.encryption_times) / len(self.encryption_times),
            'avg_decrypt': reduce(lambda x, y: x + y, self.decryption_times) / len(self.decryption_times),
            'max_encrypt': max(self.encryption_times),
            'min_encrypt': min(self.encryption_times),
            'max_decrypt': max(self.decryption_times),
            'min_decrypt': min(self.decryption_times)
        }
        return stats

    def plot_performance(self, save_path: str = None) -> None:
        """Generuje wykres wydajności szyfrowania i deszyfrowania"""
        if not self.encryption_times or not self.decryption_times:
            raise ValueError("Brak danych do wygenerowania wykresu")

        plt.figure(figsize=(10, 5))
        plt.plot(self.encryption_times, label='Szyfrowanie', marker='o')
        plt.plot(self.decryption_times, label='Deszyfrowanie', marker='x')
        plt.title(f'Wydajność algorytmu {self.__class__.__name__}')
        plt.xlabel('Numer operacji')
        plt.ylabel('Czas wykonania (s)')
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(save_path)
            print(f"Wykres zapisano do {save_path}")
        else:
            plt.show()


class CaesarCipher(Cipher):
    def __init__(self, key: str):
        super().__init__(key)
        self.shift = sum(ord(char) for char in key) % 26

    def _encrypt(self, text: str) -> str:
        """Szyfr Cezara - przesunięcie każdej litery o wartość klucza"""
        try:
            result = []
            for char in text:
                if char.isalpha():
                    shift_amount = self.shift
                    if char.islower():
                        new_char = chr(((ord(char) - ord('a') + shift_amount) % 26) + ord('a'))
                    else:
                        new_char = chr(((ord(char) - ord('A') + shift_amount) % 26) + ord('A'))
                    result.append(new_char)
                else:
                    result.append(char)
            return ''.join(result)
        except Exception as e:
            raise EncryptionError(f"Błąd podczas szyfrowania: {e}")

    def _decrypt(self, encrypted_text: str) -> str:
        """Odwrócenie szyfru Cezara"""
        try:
            result = []
            for char in encrypted_text:
                if char.isalpha():
                    shift_amount = self.shift
                    if char.islower():
                        new_char = chr(((ord(char) - ord('a') - shift_amount) % 26) + ord('a'))
                    else:
                        new_char = chr(((ord(char) - ord('A') - shift_amount) % 26) + ord('A'))
                    result.append(new_char)
                else:
                    result.append(char)
            return ''.join(result)
        except Exception as e:
            raise DecryptionError(f"Błąd podczas deszyfrowania: {e}")


class XORCipher(Cipher):
    def _encrypt(self, text: str) -> str:
        """Szyfrowanie XOR - każdy znak tekstu jest XORowany z odpowiednim znakiem klucza"""
        try:
            key_repeated = (self.key * (len(text) // len(self.key) + 1))[:len(text)]
            encrypted_bytes = [ord(t) ^ ord(k) for t, k in zip(text, key_repeated)]
            encrypted_text = base64.b64encode(bytes(encrypted_bytes)).decode('utf-8')
            return encrypted_text
        except Exception as e:
            raise EncryptionError(f"Błąd podczas szyfrowania XOR: {e}")

    def _decrypt(self, encrypted_text: str) -> str:
        """Deszyfrowanie XOR - odwrócenie operacji XOR"""
        try:
            key_repeated = (self.key * (len(encrypted_text) // len(self.key) + 1))[:len(encrypted_text)]
            encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
            decrypted_text = ''.join([chr(b ^ ord(k)) for b, k in zip(encrypted_bytes, key_repeated)])
            return decrypted_text
        except Exception as e:
            raise DecryptionError(f"Błąd podczas deszyfrowania XOR: {e}")


class ReverseCipher(Cipher):
    def _encrypt(self, text: str) -> str:
        """Odwrócenie kolejności znaków w tekście"""
        return text[::-1]

    def _decrypt(self, encrypted_text: str) -> str:
        """Odwrócenie kolejności znaków w tekście (deszyfrowanie to to samo co szyfrowanie)"""
        return encrypted_text[::-1]