import random
import gspread

class CaesarCipher:
    def __init__(self, credential_path: str = 'sheet-api-credential.json') -> None:
        self.service_account = gspread.service_account(filename = credential_path)
        self.plain_prefix = ""
        self.plain_surfix = ""
        self.full_plaintext = ""
        self.ciphertext = ""
        self.prefixes = []
        self.surfixes = []
        self.prefix_len = 0
        self.surfix_len = 0
        self.fake_option_count = 2
        self.reload_words()
        self.next_plaintext(True)
        self.encrypt()

    def reload_words(self) -> None:
        work_book = self.service_account.open("資訊科技 Sheet 應用") # title: sheet title, NOT tab name
        worksheet = work_book.worksheet("1108研習") # title: now, it's TAB name
        self.prefixes = worksheet.col_values(1)
        self.surfixes = worksheet.col_values(3)
        self.prefix_len = len(self.prefixes)
        self.surfix_len = len(self.prefixes)

    def next_plaintext(self, advanced_mode = False) -> None:
        i = random.randint(0, self.prefix_len -1)
        j = random.randint(0, self.surfix_len -1)
        self.plain_prefix = self.prefixes[i]
        self.plain_surfix = self.surfixes[j]
        if advanced_mode:
            self.full_plaintext = f"{self.plain_prefix} {self.plain_surfix}"
        else:
            self.full_plaintext = self.plain_surfix

    def encrypt(self) -> str:
        shift = random.randint(1, 5)
        result = ""
        for c in self.full_plaintext:
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
        return self.full_plaintext

    def get_question(self, advanced_mode = False) -> str:
        question = [self.ciphertext] # [0]: ciphertext
        options = self.get_options(advanced_mode) # [1~n]: 1 answer and n-1 fake
        question.extend(options)
        return ",".join(question) # "ciphertext,opt1,opt2,optn"
    
    # improve performace if have time
    def get_options(self, advanced_mode = False) -> list:
        optinos = [self.full_plaintext]
        surfix_len = len(self.plain_surfix)
        prefix_len = len(self.plain_surfix)
        valid_surfixes = [x for x in self.surfixes if len(x) == surfix_len and x != self.plain_surfix]
        random.shuffle(valid_surfixes)
        if not advanced_mode:
            optinos.extend(valid_surfixes[0:2])
            return optinos

        valid_prefixes = [x for x in self.prefixes if len(x) == prefix_len and x != self.plain_prefix]
        random.shuffle(valid_prefixes)

        for i in range(self.fake_option_count):
            prefix = valid_prefixes[i]
            surfix = valid_surfixes[i]
            optinos.append(f"{prefix} {surfix}")
        return optinos
