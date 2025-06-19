import time
import matplotlib.pyplot as plt
from cipher import CaesarCipher, XORCipher, ReverseCipher

text_sizes = [100, 1000, 10000]
def compare_ciphers_performance():
    results = {
        'Caesar': {'encrypt': [], 'decrypt': []},
        'XOR': {'encrypt': [], 'decrypt': []},
        'Reverse': {'encrypt': [], 'decrypt': []}
    }

    for size in text_sizes:
        text = 'a' * size

        # Test Caesar
        cipher = CaesarCipher("secret")
        start = time.time()
        encrypted = cipher.encrypt(text)
        results['Caesar']['encrypt'].append(time.time() - start)

        start = time.time()
        cipher.decrypt(encrypted)
        results['Caesar']['decrypt'].append(time.time() - start)

        # Test XOR
        cipher = XORCipher("secret")
        start = time.time()
        encrypted = cipher.encrypt(text)
        results['XOR']['encrypt'].append(time.time() - start)

        start = time.time()
        cipher.decrypt(encrypted)
        results['XOR']['decrypt'].append(time.time() - start)

        # Test Reverse
        cipher = ReverseCipher("secret")
        start = time.time()
        encrypted = cipher.encrypt(text)
        results['Reverse']['encrypt'].append(time.time() - start)

        start = time.time()
        cipher.decrypt(encrypted)
        results['Reverse']['decrypt'].append(time.time() - start)

    # Generowanie wykresów
    plt.figure(figsize=(12, 6))

    # Wykres szyfrowania
    plt.subplot(1, 2, 1)
    for cipher in results:
        plt.plot(text_sizes, results[cipher]['encrypt'], label=f'{cipher} encrypt', marker='o')
    plt.title('Czas szyfrowania w zależności od rozmiaru tekstu')
    plt.xlabel('Rozmiar tekstu')
    plt.ylabel('Czas (s)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)

    # Wykres deszyfrowania
    plt.subplot(1, 2, 2)
    for cipher in results:
        plt.plot(text_sizes, results[cipher]['decrypt'], label=f'{cipher} decrypt', marker='x')
    plt.title('Czas deszyfrowania w zależności od rozmiaru tekstu')
    plt.xlabel('Rozmiar tekstu')
    plt.ylabel('Czas (s)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('performance_test.png')
    print("Wykres porównawczy zapisano do performance_test.png")


if __name__ == "__main__":
    compare_ciphers_performance()