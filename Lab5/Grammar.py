class Grammar:
    EPSILON = "?"

    def __init__(self):
        self.N = []
        self.E = []
        self.S = ""
        self.P = {}

    def __processLine(self, line: str):
        # Get what comes after the '='
        return line.strip().split(' ')[2:]

    def readFromFile(self, file_name: str):
        with open(file_name) as file:
            N = self.__processLine(file.readline())
            E = self.__processLine(file.readline())
            S = self.__processLine(file.readline())[0]

            file.readline()  # P =

            # Get all transitions
            P = {}
            for line in file:
                split = line.strip().split('->')
                source = split[0]
                sequence = split[1]
                sequence_list = []
                for c in sequence:
                    sequence_list.append(c)

                if source in P.keys():
                    P[source] = P[source] + sequence_list
                else:
                    P[source] = sequence_list

            self.N = N
            self.E = E
            self.S = S
            self.P = P

    def checkCFG(self):
        hasStartingSymbol = False
        for key in self.P.keys():
            if key == self.S:
                hasStartingSymbol = True
            if key not in self.N:
                return False
        if not hasStartingSymbol:
            return False
        for rightSide in self.P.values():
            for value in rightSide:
                if value not in self.N and value not in self.E:
                    return False
        return True

    def __str__(self):
        result = "N = " + str(self.N) + "\n"
        result += "E = " + str(self.E) + "\n"
        result += "S = " + str(self.S) + "\n"
        result += "P = " + str(self.P) + "\n"
        return result
