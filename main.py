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


def get_text(cipher=None):
    """Pobiera tekst od użytkownika"""
    print("\nDostępne opcje:")
    print("1. Wprowadź tekst ręcznie")
    print("2. Wczytaj z pliku")
    print("3. Edytuj plik")

    while True:
        try:
            choice = int(input("Wybierz opcję (1-3): "))
            if choice == 1:
                return input("Wprowadź tekst: ")
            elif choice == 2:
                return handle_file_operations(cipher, 'read')
            elif choice == 3:
                edited_content = handle_file_operations(cipher, 'edit')
                if edited_content:
                    print("Zedytowana zawartość:")
                    print(edited_content)
                return edited_content
            else:
                print("Proszę wybrać 1, 2 lub 3")
        except ValueError:
            print("Proszę wprowadzić liczbę")


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


def edit_file_content(filename: str) -> str:
    """Umożliwia edycję pliku tekstowego"""
    try:
        # Otwórz plik w domyślnym edytorze systemowym
        if os.name == 'nt':  # Windows
            os.system(f'notepad "{filename}"')
        else:  # Linux/Mac
            os.system(f'nano "{filename}"')

        # Przeczytaj zmodyfikowaną zawartość
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise FileOperationError(f"Błąd podczas edycji pliku: {e}")


def handle_file_operations(cipher, operation: str):
    """Obsługa operacji na plikach z możliwością edycji"""
    filename = input("Podaj nazwę pliku: ")
    if not os.path.exists(filename):
        print("Plik nie istnieje")
        return None

    try:
        # Deszyfrowanie przed edycją
        if operation == 'edit':
            encrypted_text = cipher.read_from_file(filename)
            decrypted_text = cipher.decrypt(encrypted_text)

            # Zapisz tymczasowo odszyfrowaną wersję do edycji
            temp_file = "temp_decrypted.txt"
            cipher.save_to_file(temp_file, decrypted_text)

            # Edytuj plik
            edited_text = edit_file_content(temp_file)

            # Zaszyfruj i zapisz zmiany
            encrypted_edited = cipher.encrypt(edited_text)
            cipher.save_to_file(filename, encrypted_edited)
            os.remove(temp_file)  # Usuń plik tymczasowy
            print("Plik został pomyślnie edytowany i zaszyfrowany")
            return edited_text

        # Standardowe odczytanie pliku
        elif operation == 'read':
            content = cipher.read_from_file(filename)
            return content

    except CipherError as e:
        print(f"Błąd operacji szyfrującej: {e}")
    except Exception as e:
        print(f"Błąd operacji na pliku: {e}")
    return None

def main():
    print("=== Szyfrator wiadomości tekstowych ===")
    cipher = None

    while True:
        cipher_choice = get_cipher_choice()
        if cipher_choice == 4:
            print("Do widzenia!")
            break

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

                text = get_text(cipher)
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