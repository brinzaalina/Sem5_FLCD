from Grammar import Grammar
from Item import Item
from Parser import Parser

if __name__ == '__main__':
    g = Grammar()
    g.read_from_file("g1.in")
    g.make_enhanced_grammar()
    print(str(g))
    if g.check_cfg():
        print("The grammar is a CFG")
    else:
        print("The grammar is not a CFG")
    p = Parser(g)
    state = p.closure([Item("S'", ['S'], 0)])
    print(state)

    new_state = p.goto(state, "S")
    print(new_state)

    new_state = p.goto(state, "a")
    print(new_state)

    g2 = Grammar()
    g2.read_from_file("g3.in")
    g2.make_enhanced_grammar()
    print(str(g2))
    p2 = Parser(g2)
    state2 = p2.closure([Item(list(g2.P)[-1], g2.P[list(g2.P)[-1]][0], 0)])
    print(state2)
    print(p2.goto(state2, "E"))



