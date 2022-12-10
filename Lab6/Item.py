class Item:
    def __init__(self, lhs: str, rhs: list, dotPosition: int):
        self.lhs = lhs
        self.rhs = rhs
        self.dotPosition = dotPosition

    def __eq__(self, other):
        return self.rhs == other.rhs and \
               self.lhs == other.lhs and \
               self.dotPosition == other.dotPosition

    def __str__(self):
        result = "[" + self.lhs + " -> "
        for i in range(len(self.rhs)):
            if i == self.dotPosition:
                result += ". "
            result += self.rhs[i] + " "
        if self.dotPosition == len(self.rhs):
            result += "."
        return result.strip() + "]"
