import org.apache.commons.lang3.tuple.Pair;

public class SymbolTable {
    private int size;
    private HashTable<String> identifiersHashTable;
    private HashTable<Integer> intConstantsHashTable;
    private HashTable<String> stringConstantsHashTable;

    public SymbolTable(int size) {
        this.size = size;
        this.identifiersHashTable = new HashTable<>(size);
        this.intConstantsHashTable = new HashTable<>(size);
        this.stringConstantsHashTable = new HashTable<>(size);
    }

    public Pair<Integer, Integer> addIdentifier(String name) throws Exception {
        return identifiersHashTable.add(name);
    }

    public Pair<Integer, Integer> addIntConstant(int constant) throws Exception {
        return intConstantsHashTable.add(constant);
    }

    public Pair<Integer, Integer> addStringConstant(String constant) throws Exception {
        return stringConstantsHashTable.add(constant);
    }

    public boolean hasIdentifier(String name) {
        return identifiersHashTable.contains(name);
    }

    public boolean hasIntConstant(int constant) {
        return intConstantsHashTable.contains(constant);
    }

    public boolean hasStringConstant(String constant) {
        return stringConstantsHashTable.contains(constant);
    }

    public Pair<Integer, Integer> getPositionIdentifier(String name) {
        return identifiersHashTable.getPosition(name);
    }

    public Pair<Integer, Integer> getPositionIntConstant(int constant) {
        return intConstantsHashTable.getPosition(constant);
    }

    public Pair<Integer, Integer> getPositionStringConstant(String constant) {
        return stringConstantsHashTable.getPosition(constant);
    }

    @Override
    public String toString() {
        return "SymbolTable{" +
                "identifiersHashTable=" + identifiersHashTable +
                "\nintConstantsHashTable=" + intConstantsHashTable +
                "\nstringConstantsHashTable=" + stringConstantsHashTable +
                '}';
    }
}
