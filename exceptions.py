class CipherError(Exception):
    #Bazowy wyjątek dla wszystkich błędów związanych z szyfrowaniem
    pass

class InvalidKeyError(CipherError):
    #Wyjątek zgłaszany gdy klucz jest nieprawidłowy
    pass

class FileOperationError(CipherError):
    #Wyjątek zgłaszany gdy występuje problem z operacjami na plikach
    pass

class EncryptionError(CipherError):
    #Wyjątek zgłaszany gdy wystąpi błąd podczas szyfrowania
    pass

class DecryptionError(CipherError):
    #Wyjątek zgłaszany gdy wystąpi błąd podczas deszyfrowania
    pass