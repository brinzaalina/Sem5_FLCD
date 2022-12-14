import itertools
from enum import Enum


class ACTION(Enum):
    SHIFT = 1
    ACCEPT = 2
    REDUCE = 3
    REDUCE_REDUCE_CONFLICT = 4
    SHIFT_REDUCE_CONFLICT = 5


class State:
    id = itertools.count()

    def __init__(self, closure_items, closure, enrichedSymbol):
        self.action = None
        self.id = next(self.id)
        self.closure_items = closure_items
        self.closure = closure
        self.set_action(enrichedSymbol)

    def set_action(self, enrichedSymbol):
        if len(self.closure) == 1 and \
                len(self.closure[0].rhs) == self.closure[0].dotPosition and \
                self.closure[0].lhs == enrichedSymbol:
            self.action = ACTION.ACCEPT
        elif len(self.closure) == 1 and self.closure[0].dotPosition == len(self.closure[0].rhs):
            self.action = ACTION.REDUCE
        elif len(self.closure) != 0 and self.check_all_not_dot_end():
            self.action = ACTION.SHIFT
        else:
            if len(self.closure) > 1 and self.check_all_dot_end():
                self.action = ACTION.REDUCE_REDUCE_CONFLICT
            else:
                self.action = ACTION.SHIFT_REDUCE_CONFLICT

    def check_all_not_dot_end(self) -> bool:
        for c in self.closure:
            if len(c.rhs) <= c.dotPosition:
                return False
        return True

    def check_all_dot_end(self) -> bool:
        for c in self.closure:
            if len(c.rhs) > c.dotPosition:
                return False
        return True

    def get_all_symbols_after_dot(self):
        result = []
        for item in self.closure:
            if item.dotPosition < len(item.rhs):
                result.append(item.rhs[item.dotPosition])
        return result

    def __eq__(self, other):
        return self.closure_items == other.closure_items

    def __str__(self):
        result = "s" + str(self.id) + " = closure({"
        for item in self.closure_items:
            result += str(item) + ", "
        result = result[:-2] + "}) = {"
        for item in self.closure:
            result += str(item) + ", "
        result = result[:-2] + "}"
        return result
