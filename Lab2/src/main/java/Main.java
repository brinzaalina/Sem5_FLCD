import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;

import java.util.Objects;

public class Main {
    public static void main(String[] args) {
        SymbolTable symbolTable = new SymbolTable(47);
        Pair<Integer, Integer> p1 = new ImmutablePair<>(-1,-1);
        Pair<Integer, Integer> p2 = new ImmutablePair<>(-1,-1);
        Pair<Integer, Integer> p3 = new ImmutablePair<>(-1,-1);
        try {
            p1 = symbolTable.addIdentifier("abc");
            System.out.println("abc -> " + p1);
            System.out.println("c -> " + symbolTable.addIdentifier("c"));
            System.out.println("a -> " + symbolTable.addIdentifier("a"));
            System.out.println("bc -> " + symbolTable.addIdentifier("bc"));
            System.out.println("ba -> " + symbolTable.addIdentifier("ba"));

            System.out.println("2 -> " + symbolTable.addIntConstant(2));
            System.out.println("3 -> " + symbolTable.addIntConstant(3));
            p2 = symbolTable.addIntConstant(100);
            System.out.println("100 -> " + p2);
            System.out.println("20 -> " + symbolTable.addIntConstant(20));
            System.out.println("131 -> " + symbolTable.addIntConstant(131));
            System.out.println("49 -> " + symbolTable.addIntConstant(49));
            System.out.println("96 -> " + symbolTable.addIntConstant(96));

            System.out.println("string1 -> " + symbolTable.addStringConstant("string1"));
            System.out.println("another -> " + symbolTable.addStringConstant("another"));
            System.out.println("lab -> " + symbolTable.addStringConstant("lab"));
            System.out.println("hello -> " + symbolTable.addStringConstant("hello"));
            p3 = symbolTable.addStringConstant("world");
            System.out.println("world -> " + p3);

            System.out.println("abc -> " + symbolTable.addIdentifier("abc"));
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        System.out.println(symbolTable);

        try {
            assert symbolTable.getPositionIdentifier("abc").equals(p1) : "abc does not have position" + p1;
            assert symbolTable.getPositionIntConstant(100).equals(p2) : "100 does not have position" + p2;
            assert symbolTable.getPositionStringConstant("world").equals(p3) : "world does not have position" + p3;
            assert symbolTable.getPositionIdentifier("aaaa").equals(new ImmutablePair<>(-1, -1)) : "aaaa exists in the table";
            assert symbolTable.getPositionIntConstant(96).equals(new ImmutablePair<>(2, 2)): "96 does not have position (2, 2)";
        } catch (AssertionError e) {
            System.out.println(e.getMessage());
        }

        try {
            System.out.println("49 -> " + symbolTable.getPositionIntConstant(49));
            assert symbolTable.getPositionIntConstant(49).equals(new ImmutablePair<>(2, 2)) : "49 does not have position (2, 2)";
        } catch (AssertionError e) {
            System.out.println(e.getMessage());
        }

        try {
            System.out.println("ba -> " + symbolTable.getPositionIdentifier("ba"));
            assert symbolTable.getPositionIdentifier("ba").equals(p1) : "ba does not have position" + p1;
        } catch (AssertionError e) {
            System.out.println(e.getMessage());
        }

        try {
            System.out.println("22 -> " + symbolTable.getPositionIntConstant(22));
            assert symbolTable.getPositionIntConstant(22).equals(p2) : "22 does not have position" + p2;
        } catch (AssertionError e) {
            System.out.println(e.getMessage());
        }

        try {
            System.out.println("word -> " + symbolTable.getPositionStringConstant("word"));
            assert symbolTable.getPositionStringConstant("word").equals(p3) : "word does not have position" + p3;
        } catch (AssertionError e) {
            System.out.println(e.getMessage());
        }
    }
}
