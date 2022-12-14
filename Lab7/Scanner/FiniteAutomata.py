class StackItem:
    def __init__(self, nonTerminal: str, nonTerminalIndex: int):
        self.__nonTerminal = nonTerminal
        self.__nonTerminalIndex = nonTerminalIndex

    @property
    def NonTerminal(self):
        return self.__nonTerminal

    @NonTerminal.setter
    def NonTerminal(self, value):
        self.__nonTerminal = value

    @property
    def NonTerminalIndex(self):
        return self.__nonTerminalIndex

    @NonTerminalIndex.setter
    def NonTerminalIndex(self, value):
        self.__nonTerminalIndex = value


class FiniteAutomata:
    def __init__(self, Q: list, E: list, q0, F: list, S: dict):
        self.Q = Q
        self.E = E
        self.transitions = S
        self.q0 = q0
        self.F = F

    def isValid(self, sequence):
        if (self.q0, sequence[0]) not in self.transitions:
            return False
        stack = []
        for elem in self.transitions[(self.q0, sequence[0])]:
            stack.append((self.q0, 0, elem))
        visited = []
        while len(stack) > 0:
            current_stack_item = stack[-1]
            current_transition = (current_stack_item[0], sequence[current_stack_item[1]])
            if current_stack_item[2] in self.F and current_stack_item[1] + 1 >= len(sequence):
                return True
            stack.pop()

            if current_stack_item not in visited:
                visited.append(current_stack_item)

            next_elem_index = current_stack_item[1] + 1
            if next_elem_index >= len(sequence):
                continue
            next_transition = (current_stack_item[2], sequence[next_elem_index])
            if next_transition not in self.transitions:
                continue
            for non_terminal in self.transitions[next_transition]:
                next_stack_item = (current_stack_item[2], next_elem_index, non_terminal)
                if next_stack_item not in visited:
                    stack.append(next_stack_item)
        return False
