from collections import deque

from Parser.Grammar import Grammar
from Parser.Item import Item
from Parser.State import State, ACTION


class Connection:
    def __init__(self, starting_state: State, final_state: State, symbol: str):
        self.starting_state = starting_state
        self.final_state = final_state
        self.symbol = symbol

    def __str__(self):
        return "Starting state: " + str(self.starting_state) + " " + \
                "Final state: " + str(self.final_state) + " " + \
                "Symbol: " + str(self.symbol)


class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.canonical_collection = list()
        self.connections = []
        self.parsing_table = {}

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
                                    production[0],
                                    0
                                ), current_closure):
                            current_closure.append(
                                Item(
                                    closure_item.rhs[closure_item.dotPosition],
                                    production[0],
                                    0
                                )
                            )
            if current_closure == old_closure:
                finished = True

        return State(items, current_closure, self.grammar.S)

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
                self.connections.append(Connection(state, new_state, symbol))
            index += 1

    def create_parsing_table(self):
        for state in self.canonical_collection:
            state_connections = self.get_state_in_connections(state)
            if len(state_connections) == 0:
                if state.action == ACTION.ACCEPT:
                    self.parsing_table[state.id] = (ACTION.ACCEPT, None)
                elif state.action == ACTION.REDUCE:
                    prod_id = self.get_production_number_from_grammar(state)
                    if prod_id is None:
                        raise Exception("Somthing went wrong!")
                    self.parsing_table[state.id] = (ACTION.REDUCE, prod_id)
            elif state.action == ACTION.SHIFT or state.action == ACTION.SHIFT_REDUCE_CONFLICT:
                if state.id not in self.parsing_table.keys():
                    self.parsing_table[state.id] = (state.action, {})
                for conn in state_connections:
                    self.parsing_table[state.id][1][conn.symbol] = conn.final_state.id
            else:
                if state.action == ACTION.REDUCE_REDUCE_CONFLICT:
                    raise Exception("Reduce reduce conflict!")

    def get_production_number_from_grammar(self, state: State) -> int or None:
        for prod in self.grammar.P.keys():
            for prod_value in self.grammar.P[prod]:
                if state.closure[0].lhs == prod and state.closure[0].rhs == prod_value[0]:
                    return prod_value[1]
        return None

    def get_state_in_connections(self, state: State) -> list:
        state_connections = []
        for conn in self.connections:
            if conn.starting_state == state:
                state_connections.append(conn)
        return state_connections

    def get_state_by_id(self, state_id: int) -> State or None:
        for state in self.canonical_collection:
            if state.id == state_id:
                return state
        return None

    def get_item_with_dot_at_end(self, state: State) -> Item or None:
        for item in state.closure:
            if item.dotPosition == len(item.rhs):
                return item
        return None

    def get_production_number_shift_reduce_conflict(self, state_id: int) -> int or None:
        state = self.get_state_by_id(state_id)
        if state is None:
            return None
        item = self.get_item_with_dot_at_end(state)
        if item is None:
            return None
        for prod in self.grammar.P.keys():
            for prod_value in self.grammar.P[prod]:
                if item.lhs == prod and item.rhs == prod_value[0]:
                    return prod_value[1]
        return None

    def parse_sequence(self, words: list) -> list:
        END_SIGN = '$'
        output_band = []

        work_stack = deque()
        work_stack.append(END_SIGN)
        work_stack.append(0)

        input_stack = deque()
        input_stack.append(END_SIGN)
        for word in reversed(words):
            input_stack.append(word)

        while work_stack[-1] != END_SIGN or input_stack[-1] != END_SIGN:
            if self.parsing_table[work_stack[-1]][0] == ACTION.ACCEPT:
                while work_stack[-1] != END_SIGN:
                    work_stack.pop()
            elif self.parsing_table[work_stack[-1]][0] == ACTION.SHIFT:
                    top_state = work_stack[-1]
                    symbol = input_stack.pop()
                    work_stack.append(symbol)

                    if symbol not in self.parsing_table[top_state][1].keys():
                        raise Exception(f"Invalid symbol: {symbol} for goto of state {top_state}")

                    new_top_state = self.parsing_table[top_state][1][symbol]

                    work_stack.append(new_top_state)
            elif self.parsing_table[work_stack[-1]][0] == ACTION.SHIFT_REDUCE_CONFLICT:
                possible_symbol = input_stack[-1]
                if (len(input_stack) == 1 and input_stack[-1] == END_SIGN) or \
                        possible_symbol not in self.parsing_table[work_stack[-1]][1].keys():
                    prod_id = self.get_production_number_shift_reduce_conflict(work_stack[-1])
                    prod = self.grammar.get_production_by_id(prod_id)
                    output_band.append(prod_id)
                    index = 0
                    while index < len(prod[1]):
                        work_stack.pop()
                        work_stack.pop()
                        index += 1
                    top_state = work_stack[-1]
                    work_stack.append(prod[0])
                    new_top_state = self.parsing_table[top_state][1][prod[0]]
                    work_stack.append(new_top_state)
                else:
                    top_state = work_stack[-1]
                    symbol = input_stack.pop()
                    work_stack.append(symbol)

                    if symbol not in self.parsing_table[top_state][1].keys():
                        raise Exception(f"Invalid symbol: {symbol} for goto of state {top_state}")

                    new_top_state = self.parsing_table[top_state][1][symbol]

                    work_stack.append(new_top_state)
            elif self.parsing_table[work_stack[-1]][0] == ACTION.REDUCE:
                prod = self.grammar.get_production_by_id(
                    self.parsing_table[work_stack[-1]][1]
                )
                output_band.append(self.parsing_table[work_stack[-1]][1])
                index = 0
                while index < len(prod[1]):
                    work_stack.pop()
                    work_stack.pop()
                    index += 1
                top_state = work_stack[-1]
                work_stack.append(prod[0])
                new_top_state = self.parsing_table[top_state][1][prod[0]]
                work_stack.append(new_top_state)

        output_band.reverse()
        return output_band

