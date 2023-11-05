import random
import gspread

class CaesarCipher:
    def __init__(self, credential_path: str = 'sheet-api-credential.json') -> None:
        self.service_account = gspread.service_account(filename = credential_path)
        self.plaintext = ""
        self.ciphertext = ""
        self.prefixes = []
        self.surfixes = []
        self.prefix_len = 0
        self.surfix_len = 0
        self.reload_words()

    def reload_words(self) -> None:
        work_book = self.service_account.open("資訊科技 Sheet 應用") # title: sheet title, NOT tab name
        worksheet = work_book.worksheet("1108研習") # title: now, it's TAB name
        self.prefixes = worksheet.col_values(1)
        self.surfixes = worksheet.col_values(2)
        self.prefix_len = len(self.prefixes)
        self.surfix_len = len(self.prefixes)

    def next_plaintext(self, advanced_mode = False) -> None:
        i = random.randint(0, self.prefix_len -1)
        j = random.randint(0, self.surfix_len -1)
        prefix = self.prefixes[i]
        surfix = self.surfixes[j]
        if advanced_mode:
            self.plaintext = prefix + surfix
        else:
            self.plaintext = surfix

    def encrypt(self) -> str:
        shift = random.randint(1, 5)
        result = ""
        for c in self.plaintext:
            if c >= 'a' and c <= 'z':
                result += self.get_lower_encryption(c, shift)
            elif c >= 'A' and c <= 'Z':
                result += self.get_capital_encryption(c, shift)
            else:
                result += c
        self.ciphertext = result

    def get_lower_encryption(self, char: str, shit: int) -> str:
        code = ord(char) + shit
        if code > 122:
            code -= 26
        return chr(code)

    def get_capital_encryption(self, char: str, shit: int) -> str:
        code = ord(char) + shit
        if code > 90:
            code -= 26
        return chr(code)

    def get_plaintext(self) -> str:
        return self.plaintext

    def get_ciphertext(self) -> str:
        return self.ciphertext
