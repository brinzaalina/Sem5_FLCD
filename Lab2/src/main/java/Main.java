public class Main {
    public static void main(String[] args) {
        SymbolTable symbolTable = new SymbolTable(47);

        System.out.println("abc -> " + symbolTable.addIdentifier("abc"));
        System.out.println("c -> " + symbolTable.addIdentifier("c"));
        System.out.println("a -> " + symbolTable.addIdentifier("a"));
        System.out.println("bc -> " + symbolTable.addIdentifier("bc"));
        System.out.println("ba -> " + symbolTable.addIdentifier("ba"));

        System.out.println("2 -> " + symbolTable.addIntConstant(2));
        System.out.println("3 -> " +symbolTable.addIntConstant(3));
        System.out.println("100 -> " +symbolTable.addIntConstant(100));
        System.out.println("20 -> " + symbolTable.addIntConstant(20));
        System.out.println("131 -> " + symbolTable.addIntConstant(131));

        System.out.println("string1" + symbolTable.addStringConstant("string1"));
        System.out.println("another" + symbolTable.addStringConstant("another"));
        System.out.println("lab" + symbolTable.addStringConstant("lab"));
        System.out.println("hello" + symbolTable.addStringConstant("hello"));
        System.out.println("world" +symbolTable.addStringConstant("world"));

        System.out.println(symbolTable);

        System.out.println("abc -> " + symbolTable.addIdentifier("abc"));
    }
}
