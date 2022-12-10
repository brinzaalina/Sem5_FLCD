from Grammar import Grammar
from Item import Item
from Parser import Parser

if __name__ == '__main__':
    g = Grammar()
    g.read_from_file("g2.in")
    print(g)
    g.make_enhanced_grammar()
    parser = Parser(g)
    parser.create_canonical_collection()
    for state in parser.canonical_collection:
        print(state)
