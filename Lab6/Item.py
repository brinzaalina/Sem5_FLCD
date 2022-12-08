class Item:
    def __init__(self, lhs, rhs, dotPosition):
        self.lhs = lhs
        self.rhs = rhs
        self.dotPosition = dotPosition

    def __str__(self):
        result = "[" + self.lhs + " -> "
        for i in range(len(self.rhs)):
            if i == self.dotPosition:
                result += ". "
            result += self.rhs[i] + " "
        if self.dotPosition == len(self.rhs):
            result += "."
        return result.strip() + "]"
