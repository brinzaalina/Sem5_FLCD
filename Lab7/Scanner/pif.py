class Pif:
    def __init__(self):
        self.__pairs = []

    def insert(self, token, pos):
        self.__pairs.append((token, pos))

    @property
    def Tokens(self):
        return self.__pairs

    def __str__(self):
        text = ""
        for pair in self.__pairs:
            text += pair[0] + " --> (" + str(pair[1][0]) + "," + str(pair[1][1]) + ")" + "\n"
        return text
