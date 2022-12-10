from Grammar import Grammar
from Item import Item
from State import State


class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.canonical_collection = list()

    @staticmethod
    def is_item_in_closure(item, closure):
        for itemInClosure in closure:
            if item.lhs == itemInClosure.lhs and \
                    item.rhs == itemInClosure.rhs and \
                    item.dotPosition == itemInClosure.dotPosition:
                return True
        return False

    def closure(self, items: list) -> State:
        current_closure = items.copy()

        finished = False
        while not finished:
            old_closure = current_closure.copy()
            for closure_item in current_closure:
                if closure_item.dotPosition < len(closure_item.rhs) and \
                        closure_item.rhs[closure_item.dotPosition] in self.grammar.N:
                    for production in self.grammar.P[closure_item.rhs[closure_item.dotPosition]]:
                        if not self.is_item_in_closure(
                                Item(
                                    closure_item.rhs[closure_item.dotPosition],
                                    production,
                                    0
                                ), current_closure):
                            current_closure.append(
                                Item(
                                    closure_item.rhs[closure_item.dotPosition],
                                    production,
                                    0
                                )
                            )
            if current_closure == old_closure:
                finished = True

        return State(items, current_closure)

    def goto(self, state: State, symbol: str) -> State:
        items_for_symbol = []
        for item in state.closure:
            if item.dotPosition < len(item.rhs) \
                    and item.rhs[item.dotPosition] == symbol:
                items_for_symbol.append(Item(item.lhs, item.rhs, item.dotPosition + 1))
        for the_state in self.canonical_collection:
            if the_state.closure_items == items_for_symbol:
                return the_state
        return self.closure(items_for_symbol)

    def create_canonical_collection(self):
        self.canonical_collection = [
            self.closure(
                [Item(
                    self.grammar.S,
                    self.grammar.P[self.grammar.S][0],
                    0
                )]
            )
        ]
        index = 0
        while index < len(self.canonical_collection):
            state = self.canonical_collection[index]
            symbols = state.get_all_symbols_after_dot()
            for symbol in symbols:
                new_state = self.goto(state, symbol)
                if new_state not in self.canonical_collection:
                    self.canonical_collection.append(new_state)
            index += 1
