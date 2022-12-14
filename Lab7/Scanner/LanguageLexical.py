from Scanner.hash_table import HashTable


class LanguageLexical:
    def __init__(self):
        self.__separators = HashTable()
        self.__operators = HashTable()
        self.__reserved_words = HashTable()
        self.__initialize()

    @property
    def separators(self):
        return self.__separators

    @property
    def operators(self):
        return self.__operators

    @property
    def reserved_words(self):
        return self.__reserved_words

    def __initialize(self):
        self.__read_operators("Scanner/program/operators.in")
        self.__read_separators("Scanner/program/separators.in")
        self.__read_reserved_words("Scanner/program/reserved_words.in")

    def __read_operators(self, file_name: str):
        file = open(file_name, "r")
        for line in file:
            self.__operators.insert(line[:-1])

    def __read_separators(self, file_name: str):
        file = open(file_name, "r")
        for line in file:
            self.__separators.insert(line[:-1])
        self.__separators.insert(" ")
        self.__separators.insert("\n")
        self.__separators.insert("\r")
        self.__separators.insert("\t")

    def __read_reserved_words(self, file_name: str):
        file = open(file_name, "r")
        for line in file:
            self.__reserved_words.insert(line[:-1])
