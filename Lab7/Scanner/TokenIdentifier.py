import re
from re import match

from Scanner.LanguageLexical import LanguageLexical
from Scanner.Utils import Utils
from Scanner.hash_table import HashTable
from Scanner.pif import Pif


class TokenIdentifier:
    STRING_CONSTANT = "string_constant"
    INTEGER_CONSTANT = "integer_constant"
    IDENTIFIER = "identifier"
    separators = ["\n", "#", ",", "|", "[", "]", "(", ")"]

    def __init__(self, languageLexical: LanguageLexical):
        self.__languageLexical = languageLexical
        self.__symbolTable = HashTable()
        self.__pif = Pif()
        self.__utils = Utils()
        self.__identifierFA = self.__utils.readFromFile('Scanner/program/identifier_FA.in')
        self.__is_integer_constantFA = self.__utils.readFromFile('Scanner/program/integer_constant_FA.in')
        self.__is_string_FA = self.__utils.readFromFile("Scanner/program/stringFA.in")

    @property
    def Pif(self):
        return self.__pif

    def is_identifier(self, token: str) -> bool:
        return self.__identifierFA.isValid(token)

    def is_integer_constant(self, token: str) -> bool:
        return self.__is_integer_constantFA.isValid(token)

    def is_string_constant(self, token: str) -> bool:
        return match(r'^"(.*)"$', token) is not None

    def is_reserved_word(self, token: str) -> bool:
        return self.__languageLexical.reserved_words.get(token)

    def is_operator(self, token: str) -> bool:
        return self.__languageLexical.operators.get(token)

    def __get_split_string(self):
        split_string = ""
        for separator in self.__languageLexical.separators.get_all_keys():
            split_string += "[" + separator + "]" + "|"
        return split_string[:-1]

    def find(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def create_token_list(self, line: str) -> list:
        tokens = []
        current_token = ""
        for character in line:
            if character == " ":
                if current_token == "":
                    continue
                current_token = current_token.strip()
                if current_token != "":
                    tokens.append(current_token)
                current_token = ""
            if character in self.separators:
                current_token = current_token.strip()
                if current_token != '':
                    tokens.append(current_token)
                tokens.append(str(character))
                current_token = ""
            else:
                current_token += character
        current_token = current_token.strip()
        if current_token != "":
            tokens.append(current_token)
        return tokens

    def read_tokens(self, program_file):
        current_line = 1
        split_string = self.__get_split_string()

        is_correct = True
        invalid_token = ""
        for line in program_file:
            ' '.join(line.split())
            tokens = self.create_token_list(line)
            if not tokens:
                continue
            print(tokens)

            for token in tokens:
                if token == " ":
                    continue
                if token == '\n':
                    self.insert_separator("\\n")
                    continue
                if token in self.separators:
                    self.insert_separator(token)
                    continue

                is_token_correct = False
                is_token_correct = is_token_correct or self.is_reserved_word(token)
                if is_token_correct:
                    self.insert_other(token)
                    continue

                is_token_correct = is_token_correct or self.is_operator(token)
                if is_token_correct:
                    self.insert_other(token)
                    continue

                is_token_correct = is_token_correct or self.is_identifier(token)
                if is_token_correct:
                    self.insert_token(token, self.IDENTIFIER)
                    continue

                is_token_correct = is_token_correct or self.is_integer_constant(token)
                if is_token_correct:
                    self.insert_token(token, self.INTEGER_CONSTANT)
                    continue

                is_token_correct = is_token_correct or self.is_string_constant(token)
                if is_token_correct:
                    self.insert_token(token, self.STRING_CONSTANT)
                    continue

                if not is_token_correct:
                    invalid_token = token
                    is_correct = False
                    break

            if not is_correct:
                break
            current_line += 1
        if is_correct:
            print("Program is lexically correct!")
        else:
            print(f"Lexical error at line {current_line} on {invalid_token}!")
        st_file = open("ST.out", "w")
        st_file.write(str(self.__symbolTable))
        st_file.close()

        pif_file = open("PIF.out", "w")
        pif_file.write(str(self.__pif))
        pif_file.close()

    def insert_separator(self, separator: str):
        self.__pif.insert(separator, (-1, -1))

    def insert_other(self, token: str):
        self.__pif.insert(token, (-1, -1))

    def insert_token(self, token: str, the_type: str):
        try:
            num1, num2 = self.__symbolTable.insert(token)
            self.__pif.insert(the_type, (num1, num2))
        except Exception:
            pass

