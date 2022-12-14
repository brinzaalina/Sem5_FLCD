from Scanner.FiniteAutomata import FiniteAutomata


class Utils:
    def __processLine(self, line: str):
        # Get what comes after the '='
        return line.strip().split(' ')[2:]

    def readFromFile(self, file_name: str):
        with open(file_name) as file:
            Q = self.__processLine(file.readline())
            E = self.__processLine(file.readline())
            q0 = self.__processLine(file.readline())[0]
            F = self.__processLine(file.readline())

            file.readline()  # delta =

            # Get all transitions
            delta = {}
            for line in file:
                split = line.strip().split('=>')
                source = split[0].strip().replace('(', '').replace(')', '').split(',')[0]
                route = split[0].strip().replace('(', '').replace(')', '').split(',')[1]
                destination = split[1].strip()

                if (source, route) in delta.keys():
                    delta[(source, route)].append(destination)
                else:
                    delta[(source, route)] = [destination]

            return FiniteAutomata(Q, E, q0, F, delta)
