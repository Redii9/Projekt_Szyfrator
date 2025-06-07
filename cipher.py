import os
import base64
from typing import Callable
from exceptions import *

class Cipher:
    def __init__(self, key: str):
        if not key or not isinstance(key, str):
            raise InvalidKeyError("Klucz musi być niepustym ciągiem znaków")
        self.key = key

    def encrypt(self, text: str) -> str:
        #Szyfruje tekst przy użyciu klucza
        raise NotImplementedError("Metoda encrypt musi być zaimplementowana w klasie pochodnej")

    def decrypt(self, encrypted_text: str) -> str:
        #Deszyfruje tekst przy użyciu klucza
        raise NotImplementedError("Metoda decrypt musi być zaimplementowana w klasie pochodnej")

    def save_to_file(self, filename: str, text: str) -> None:
        #Zapisuje tekst do pliku
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
        except (IOError, OSError) as e:
            raise FileOperationError(f"Błąd podczas zapisu do pliku: {e}")

    def read_from_file(self, filename: str) -> str:
        #Odczytuje tekst z pliku
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except (IOError, OSError) as e:
            raise FileOperationError(f"Błąd podczas odczytu z pliku: {e}")

    @staticmethod
    def apply_lambda_operation(text: str, operation: Callable[[str], str]) -> str:
        #Stosuje operację lambda na tekście
        return operation(text)


class CaesarCipher(Cipher):
    def __init__(self, key: str):
        super().__init__(key)
        self.shift = sum(ord(char) for char in key) % 26

    def encrypt(self, text: str) -> str:
        #Szyfr Cezara - przesunięcie każdej litery o wartość klucza
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

    def decrypt(self, encrypted_text: str) -> str:
        #Odwrócenie szyfru Cezara
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
    def encrypt(self, text: str) -> str:
        #Szyfrowanie XOR - każdy znak tekstu jest XORowany z odpowiednim znakiem klucza
        try:
            key_repeated = (self.key * (len(text) // len(self.key) + 1))[:len(text)]
            encrypted_bytes = [ord(t) ^ ord(k) for t, k in zip(text, key_repeated)]
            encrypted_text = base64.b64encode(bytes(encrypted_bytes)).decode('utf-8')
            return encrypted_text
        except Exception as e:
            raise EncryptionError(f"Błąd podczas szyfrowania XOR: {e}")

    def decrypt(self, encrypted_text: str) -> str:
        #Deszyfrowanie XOR - odwrócenie operacji XOR
        try:
            key_repeated = (self.key * (len(encrypted_text) // len(self.key) + 1))[:len(encrypted_text)]
            encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
            decrypted_text = ''.join([chr(b ^ ord(k)) for b, k in zip(encrypted_bytes, key_repeated)])
            return decrypted_text
        except Exception as e:
            raise DecryptionError(f"Błąd podczas deszyfrowania XOR: {e}")


class ReverseCipher(Cipher):
    def encrypt(self, text: str) -> str:
        #Odwrócenie kolejności znaków w tekście
        return text[::-1]

    def decrypt(self, encrypted_text: str) -> str:
        #Odwrócenie kolejności znaków w tekście (deszyfrowanie to to samo co szyfrowanie)
        return encrypted_text[::-1]