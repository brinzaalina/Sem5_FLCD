from Item import Item
from State import State


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

    @staticmethod
    def is_item_in_closure(item, closure):
        for itemInClosure in closure:
            if item.lhs == itemInClosure.lhs and \
                    item.rhs == itemInClosure.rhs and \
                    item.dotPosition == itemInClosure.dotPosition:
                return True
        return False

    def closure(self, items):
        current_closure = list(items)
        for index in range(len(items)):
            item = items[index]
            if item.dotPosition == len(item.rhs):
                return State(items, current_closure)

            if (item.rhs[item.dotPosition] not in self.grammar.N) and (item.rhs[item.dotPosition] not in self.grammar.E):
                return None

            while True:
                old_closure = current_closure.copy()
                for closure_item in current_closure:
                    if closure_item.rhs[closure_item.dotPosition] in self.grammar.N:
                        for production in self.grammar.P[closure_item.rhs[closure_item.dotPosition]]:
                            if not self.is_item_in_closure(Item(closure_item.rhs[closure_item.dotPosition], production, 0), current_closure):
                                current_closure.append(Item(closure_item.rhs[closure_item.dotPosition], production, 0))
                if current_closure == old_closure:
                    break
        return State(items, current_closure)

    def goto(self, state, symbol):
        items_for_symbol = []
        for item in state.closure:
            if item.rhs[item.dotPosition] == symbol:
                items_for_symbol.append(Item(item.lhs, item.rhs, item.dotPosition + 1))
        return self.closure(items_for_symbol)

