from hash_table import HashTable


class Scanner:
    __identifiers_st: HashTable
    __constants_st: HashTable

    def __init__(self):
        self.__identifiers_st = HashTable()
        self.__constants_st = HashTable()

    def add_constants(self, file_name):
        file = open(file_name, "r")
        for line in file:
            self.__constants_st.insert(line[:-1])
