from Parser.Grammar import Grammar
from Parser.Parser import Parser
from Parser.ParserOutput import ParserOutput
from Scanner.LanguageLexical import LanguageLexical
from Scanner.TokenIdentifier import TokenIdentifier

if __name__ == '__main__':
    lexical = LanguageLexical()
    token_identifier = TokenIdentifier(lexical)

    print("Analyzing p3...")
    p1_source = open("examples/p2.in", "r")
    token_identifier.read_tokens(p1_source)

    tokens = []
    for item in token_identifier.Pif.Tokens:
        tokens.append(item[0])

    # print(token_identifier.Pif)

    g = Grammar()
    g.read_from_file("g2.in")
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
    output_band = parser.parse_sequence(tokens)
    print(output_band)

    parserOutput = ParserOutput(output_band, g)
    parserOutput.compute_parsing_tree()
    for item in parserOutput.paring_tree:
        print(item)
