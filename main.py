from cipher import CaesarCipher, XORCipher, ReverseCipher
from exceptions import CipherError
import os
import time


def get_cipher_choice():
    #Menu
    print("\nDostępne szyfry:")
    print("1. Szyfr Cezara")
    print("2. Szyfr XOR")
    print("3. Odwrócony tekst")
    print("4. Wyjście")

    while True:
        try:
            choice = int(input("Wybierz szyfr (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Proszę wybrać liczbę od 1 do 4")
        except ValueError:
            print("Proszę wprowadzić liczbę")


def get_operation_choice():
    #Wybór operacji od użytkownika
    print("\nDostępne operacje:")
    print("1. Szyfrowanie")
    print("2. Deszyfrowanie")
    print("3. Powrót")

    while True:
        try:
            choice = int(input("Wybierz operację (1-3): "))
            if 1 <= choice <= 3:
                return choice
            print("Proszę wybrać liczbę od 1 do 3")
        except ValueError:
            print("Proszę wprowadzić liczbę")


def get_key():
    #Pobiera klucz od użytkownika
    while True:
        key = input("Podaj klucz szyfrowania: ")
        if key:
            return key
        print("Klucz nie może być pusty")


def get_text():
    #Pobiera tekst od użytkownika
    print("\nDostępne opcje:")
    print("1. Wprowadź tekst ręcznie")
    print("2. Wczytaj z pliku")

    while True:
        try:
            choice = int(input("Wybierz opcję (1-2): "))
            if choice == 1:
                return input("Wprowadź tekst: ")
            elif choice == 2:
                filename = input("Podaj nazwę pliku: ")
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as file:
                        return file.read()
                print("Plik nie istnieje")
            else:
                print("Proszę wybrać 1 lub 2")
        except ValueError:
            print("Proszę wprowadzić liczbę")
        except IOError as e:
            print(f"Błąd odczytu pliku: {e}")


def save_to_file(text):
    #Zapisanie wyniku do pliku
    choice = input("Czy chcesz zapisać wynik do pliku? (t/n): ").lower()
    if choice == 't':
        filename = input("Podaj nazwę pliku: ")
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Tekst został zapisany do pliku {filename}")
        except IOError as e:
            print(f"Błąd zapisu do pliku: {e}")


def apply_lambda_operations(cipher, text):
    #Użycie funkcji lambda
    print("\nUżycie funkcji lambda:")

    # Lambda do zamiany na wielkie litery
    upper = lambda x: x.upper()
    print(f"Tekst wielkimi literami: {cipher.apply_lambda_operation(text, upper)}")

    # Lambda do odwrócenia tekstu
    reverse = lambda x: x[::-1]
    print(f"Odwrócony tekst: {cipher.apply_lambda_operation(text, reverse)}")

    # Lambda do usunięcia spacji
    no_spaces = lambda x: x.replace(" ", "")
    print(f"Tekst bez spacji: {cipher.apply_lambda_operation(text, no_spaces)}")


def show_performance_stats(cipher):
    """Wyświetla statystyki wydajności szyfrowania"""
    stats = cipher.get_performance_stats()
    if stats:
        print("\nStatystyki wydajności:")
        print(f"Średni czas szyfrowania: {stats['avg_encrypt']:.6f}s")
        print(f"Średni czas deszyfrowania: {stats['avg_decrypt']:.6f}s")
        print(f"Minimalny czas szyfrowania: {stats['min_encrypt']:.6f}s")
        print(f"Maksymalny czas szyfrowania: {stats['max_encrypt']:.6f}s")
        print(f"Minimalny czas deszyfrowania: {stats['min_decrypt']:.6f}s")
        print(f"Maksymalny czas deszyfrowania: {stats['max_decrypt']:.6f}s")

        choice = input("\nCzy chcesz wygenerować wykres wydajności? (t/n): ").lower()
        if choice == 't':
            filename = input("Podaj nazwę pliku do zapisu wykresu (lub pozostaw puste aby wyświetlić): ")
            if not filename:
                cipher.plot_performance()
            else:
                if not filename.endswith('.png'):
                    filename += '.png'
                cipher.plot_performance(filename)
    else:
        print("Brak danych o wydajności. Wykonaj najpierw operacje szyfrowania/deszyfrowania.")


def benchmark_cipher(cipher_class, key, text, iterations=100):
    """Test wydajnościowy dla danego szyfru"""
    print(f"\nRozpoczynam test wydajności dla {cipher_class.__name__}...")
    cipher = cipher_class(key)

    # Test szyfrowania
    start_time = time.time()
    for _ in range(iterations):
        cipher.encrypt(text)
    encrypt_time = time.time() - start_time

    # Test deszyfrowania
    encrypted = cipher.encrypt(text)
    start_time = time.time()
    for _ in range(iterations):
        cipher.decrypt(encrypted)
    decrypt_time = time.time() - start_time

    print(f"Wyniki dla {iterations} iteracji:")
    print(f"Całkowity czas szyfrowania: {encrypt_time:.4f}s")
    print(f"Średni czas szyfrowania: {encrypt_time / iterations:.6f}s")
    print(f"Całkowity czas deszyfrowania: {decrypt_time:.4f}s")
    print(f"Średni czas deszyfrowania: {decrypt_time / iterations:.6f}s")

def main():
    print("=== Szyfrator wiadomości tekstowych ===")

    while True:
        cipher_choice = get_cipher_choice()
        if cipher_choice == 4:
            print("Do widzenia!")
            break

        cipher = None
        try:
            if cipher_choice == 1:
                cipher = CaesarCipher(get_key())
            elif cipher_choice == 2:
                cipher = XORCipher(get_key())
            elif cipher_choice == 3:
                cipher = ReverseCipher(get_key())

            if cipher_choice in (1, 2, 3):
                choice = input("Czy chcesz wykonać test wydajności? (t/n): ").lower()
                if choice == 't':
                    text = "Testowy tekst do pomiaru wydajnosci algorytmu." * 10
                    benchmark_cipher(cipher.__class__, cipher.key, text)
                    continue

            while True:
                operation_choice = get_operation_choice()
                if operation_choice == 3:
                    break

                text = get_text()
                if not text:
                    print("Tekst nie może być pusty")
                    continue

                try:
                    if operation_choice == 1:  # Szyfrowanie
                        result = cipher.encrypt(text)
                        print("\nZaszyfrowany tekst:", result)
                    elif operation_choice == 2:  # Deszyfrowanie
                        result = cipher.decrypt(text)
                        print("\nOdszyfrowany tekst:", result)

                    save_to_file(result)
                    apply_lambda_operations(cipher, result)

                    show_performance_stats(cipher)

                except CipherError as e:
                    print(f"Błąd: {e}")

        except CipherError as e:
            print(f"Błąd inicjalizacji szyfru: {e}")


if __name__ == "__main__":
    main()