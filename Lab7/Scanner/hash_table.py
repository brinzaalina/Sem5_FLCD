class HashTable:
    __start_size = 5
    __size = 0
    __elements: []
    __array_of_elements_size = 0

    def __init__(self):
        self.__elements = [[] for _ in range(self.__start_size)]
        self.__size = 0
        self.__array_of_elements_size = self.__start_size

    def __compute_hash(self, key: str) -> int:
        """
        Computes the hash value of the given key
        :param key: The key
        :return: The hash value
        """
        char_sum = 0
        for char in key:
            char_sum += ord(char) - ord('0')
        return char_sum % self.__array_of_elements_size

    def __rehash_table(self):
        """
        Rehash the table
        """
        self.__array_of_elements_size *= 2
        new_elements = [[] for _ in range(self.__array_of_elements_size)]
        for list_item in self.__elements:
            for key in list_item:
                hash_value = self.__compute_hash(key)
                new_elements[hash_value].append(key)
        self.__elements = new_elements

    def __check_key_existence(self, key: str, hash_value: int) -> bool:
        """
        Checks if a key is already in the hash table
        :param key: The key to be searched
        :param hash_value: hash value of the key
        :return: True if the key exists, False otherwise
        """
        for keys in self.__elements[hash_value]:
            if key == keys:
                return True
        return False

    def insert(self, key: str):
        """
        Insert a key into the hash table
        :param key: The key to be added
        """
        if self.__size / self.__array_of_elements_size > 0.6:
            self.__rehash_table()
        hash_value = self.__compute_hash(key)
        # check if the key is not already added
        if not self.__check_key_existence(key, hash_value):
            self.__elements[hash_value].append(key)
            self.__size += 1
        return hash_value, len(self.__elements[hash_value]) - 1

    def remove(self, key: str):
        """
        Removes a key from the hash table
        :param key: The key to be removed
        :exception If the key does not exist
        """
        hash_value = self.__compute_hash(key)
        for elem_key in self.__elements[hash_value]:
            if elem_key == key:
                self.__elements[hash_value].remove(key)
                return
        raise Exception("Key does not exist")

    def get(self, key: str) -> bool:
        """
        Checks whether a key exists or not
        :param key: The key to be checked
        :return: True if it exists, False otherwise
        """
        hash_value = self.__compute_hash(key)
        return key in self.__elements[hash_value]

    def get_all_keys(self) -> []:
        keys = []
        for elem in self.__elements:
            for value in elem:
                keys.append(value)
        return keys

    def get_location(self, key):
        hash_value = self.__compute_hash(key)
        for index in range(len(self.__elements[hash_value])):
            if self.__elements[hash_value][index] == key:
                return hash_value, index

    def __str__(self):
        result = ""
        for index in range(len(self.__elements)):
            if not self.__elements[index]:
                continue
            for index2 in range(len(self.__elements[index])):
                result += \
                    "(" + str(index) + ", " \
                    + str(index2) + ")" + "->" + self.__elements[index][index2] \
                    + "\n"
        return result
