import unittest
import time
from cipher import CaesarCipher, XORCipher, ReverseCipher
from exceptions import *


class TestCiphers(unittest.TestCase):
    def setUp(self):
        self.test_text = "Ala ma kota, a kot ma Ale!"
        self.caesar = CaesarCipher("secret")
        self.xor = XORCipher("secret")
        self.reverse = ReverseCipher("secret")

    def test_caesar_encrypt_decrypt(self):
        encrypted = self.caesar.encrypt(self.test_text)
        decrypted = self.caesar.decrypt(encrypted)
        self.assertEqual(decrypted, self.test_text)

    def test_xor_encrypt_decrypt(self):
        encrypted = self.xor.encrypt(self.test_text)
        decrypted = self.xor.decrypt(encrypted)
        self.assertEqual(decrypted, self.test_text)

    def test_reverse_encrypt_decrypt(self):
        encrypted = self.reverse.encrypt(self.test_text)
        decrypted = self.reverse.decrypt(encrypted)
        self.assertEqual(decrypted, self.test_text)

    def test_invalid_key(self):
        with self.assertRaises(InvalidKeyError):
            CaesarCipher("")
        with self.assertRaises(InvalidKeyError):
            XORCipher(123)

    def test_file_operations(self):
        filename = "test.txt"
        try:
            self.caesar.save_to_file(filename, self.test_text)
            content = self.caesar.read_from_file(filename)
            self.assertEqual(content, self.test_text)
        finally:
            import os
            if os.path.exists(filename):
                os.remove(filename)

    def test_lambda_operations(self):
        upper = lambda x: x.upper()
        result = self.caesar.apply_lambda_operation(self.test_text, upper)
        self.assertEqual(result, self.test_text.upper())

    def test_filter_text(self):
        is_alpha = lambda x: x.isalpha() or x == ' '
        result = self.caesar.filter_text(self.test_text, is_alpha)
        expected = 'Ala ma kota a kot ma Ale'
        self.assertEqual(result, expected)

    def test_map_text(self):
        to_upper = lambda x: x.upper()
        result = self.caesar.map_text(self.test_text, to_upper)
        self.assertEqual(result, self.test_text.upper())

    def test_performance_stats(self):
        # Wykonaj kilka operacji aby zebrać dane
        for _ in range(5):
            self.caesar.encrypt(self.test_text)
            self.caesar.decrypt(self.caesar.encrypt(self.test_text))

        stats = self.caesar.get_performance_stats()
        self.assertIn('avg_encrypt', stats)
        self.assertIn('avg_decrypt', stats)


class TestIntegration(unittest.TestCase):
    def test_multiple_ciphers(self):
        text = "Integracja roznych szyfrow"
        caesar = CaesarCipher("1")
        xor = XORCipher("2")
        reverse = ReverseCipher("3")

        # Szyfrowanie wielokrotne
        encrypted = caesar.encrypt(text)
        encrypted = xor.encrypt(encrypted)
        encrypted = reverse.encrypt(encrypted)

        # Deszyfrowanie w odwrotnej kolejności
        decrypted = reverse.decrypt(encrypted)
        decrypted = xor.decrypt(decrypted)
        decrypted = caesar.decrypt(decrypted)

        self.assertEqual(decrypted, text)


if __name__ == "__main__":
    unittest.main()