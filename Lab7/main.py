from Parser.Grammar import Grammar
from Parser.Parser import Parser
from Parser.ParserOutput import ParserOutput
from Scanner.LanguageLexical import LanguageLexical
from Scanner.TokenIdentifier import TokenIdentifier


def run_for_g1():
    g = Grammar()
    g.read_from_file("g1.in")
    print(g)
    g.make_enhanced_grammar()
    parser = Parser(g)
    parser.create_canonical_collection()
    for state in parser.canonical_collection:
        print(state)

    parser.create_parsing_table()

    print(parser.parsing_table)

    print("Enter a sequence: ")
    sequence = input()
    output_band = parser.parse_sequence(sequence.split(" "))

    # output_band = parser.parse_sequence(['a', 'b', 'b', 'c'])
    print(output_band)

    parserOutput = ParserOutput(output_band, g)
    parserOutput.compute_parsing_tree()
    for item in parserOutput.parsing_tree:
        print(item)

    parserOutput.print_to_file("out1.txt")


def run_for_g2():
    lexical = LanguageLexical()
    token_identifier = TokenIdentifier(lexical)

    print("Analyzing p2...")
    p1_source = open("examples/p1.in", "r")
    token_identifier.read_tokens(p1_source)

    tokens = []
    for item in token_identifier.Pif.Tokens:
        tokens.append(item[0])

    g = Grammar()
    g.read_from_file("g2.in")
    print(g)
    g.make_enhanced_grammar()
    parser = Parser(g)
    parser.create_canonical_collection()
    for state in parser.canonical_collection:
        print(state)

    parser.create_parsing_table()

    print(parser.parsing_table)

    output_band = parser.parse_sequence(tokens)
    print(output_band)

    parserOutput = ParserOutput(output_band, g)
    parserOutput.compute_parsing_tree()
    for item in parserOutput.parsing_tree:
        print(item)

    parserOutput.print_to_file("out2.txt")


if __name__ == '__main__':
    run_for_g1()
