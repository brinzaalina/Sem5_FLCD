from Grammar import Grammar
from Item import Item
from Parser import Parser
from ParserOutput import ParserOutput

if __name__ == '__main__':
    g = Grammar()
    g.read_from_file("../g2.in")
    print(g)
    g.make_enhanced_grammar()
    parser = Parser(g)
    parser.create_canonical_collection()
    for state in parser.canonical_collection:
        print(state)

    # for conn in parser.connections:
    #     print(conn)

    parser.create_parsing_table()

    print(parser.parsing_table)

    # output_band = parser.parse_sequence(['a', 'b', 'b', 'c'])
    output_band = parser.parse_sequence(['identifier', '=', 'integer_constant'])
    print(output_band)

    parserOutput = ParserOutput(output_band, g)
    parserOutput.compute_parsing_tree()
    for item in parserOutput.paring_tree:
        print(item)



