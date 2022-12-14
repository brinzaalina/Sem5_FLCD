from Parser.Grammar import Grammar


class ParserOutputEntry:
    def __init__(self, index: int, symbol: int, father: int, sibling: int):
        self.__index = index
        self.__symbol = symbol
        self.__father = father
        self.__sibling = sibling

    @property
    def Index(self):
        return self.__index

    @Index.setter
    def Index(self, value):
        self.__index = value

    @property
    def Symbol(self):
        return self.__symbol

    @Symbol.setter
    def Symbol(self, value):
        self.__symbol = value

    @property
    def Father(self):
        return self.__father

    @Father.setter
    def Father(self, value):
        self.__father = value

    @property
    def Sibling(self):
        return self.__sibling

    @Sibling.setter
    def Sibling(self, value):
        self.__sibling = value

    def __str__(self):
        return f"({self.__index}, {self.__symbol}, {self.__father}, {self.__sibling})"


class ParserOutput:

    def __init__(self, output_band: list, grammar: Grammar):
        self.output_band = output_band
        self.paring_tree = []
        self.grammar = grammar

    def __check_has_children(self, node) -> bool:
        for item in self.paring_tree:
            if item.Father == node:
                return True
        return False

    def compute_parsing_tree(self):
        current_index = 0
        self.paring_tree.append(
            ParserOutputEntry(current_index, self.grammar.initial_starting_symbol, -1, -1)
        )
        for production_id in self.output_band:
            production = self.grammar.get_production_by_id(production_id)
            for parsing_tree_item in self.paring_tree:
                if parsing_tree_item.Symbol == production[0] \
                        and not self.__check_has_children(parsing_tree_item.Index):
                    father = parsing_tree_item.Index
                    current_index += 1
                    self.paring_tree.append(
                        ParserOutputEntry(current_index, production[1][0], father, -1)
                    )
                    for index in range(1, len(production[1])):
                        current_index += 1
                        self.paring_tree[current_index - 1].Sibling = current_index
                        self.paring_tree.append(
                            ParserOutputEntry(
                                current_index,
                                production[1][index],
                                father,
                                -1
                            )
                        )
                    break
