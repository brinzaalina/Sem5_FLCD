import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class Scanner {
    private final String program;
    private List<String> tokens;
    private SymbolTable symbolTable;
    private List<Pair<Integer, Pair<Integer, Integer>>> PIF;
    private int index = 0;
    private int currentLine = 1;

    public Scanner(String program) {
        this.program = program;
        this.symbolTable = new SymbolTable(47);
        this.PIF = new ArrayList<>();
    }

    public List<String> getTokens() {
        return tokens;
    }

    public void setTokens(List<String> tokens) {
        this.tokens = tokens;
    }

    public SymbolTable getSymbolTable() {
        return symbolTable;
    }

    public void setSymbolTable(SymbolTable symbolTable) {
        this.symbolTable = symbolTable;
    }

    public List<Pair<Integer, Pair<Integer, Integer>>> getPIF() {
        return PIF;
    }

    public void setPIF(List<Pair<Integer, Pair<Integer, Integer>>> PIF) {
        this.PIF = PIF;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }

    public int getCurrentLine() {
        return currentLine;
    }

    public void setCurrentLine(int currentLine) {
        this.currentLine = currentLine;
    }

    private void skipSpaces() {
        while (index < program.length() && Character.isWhitespace(program.charAt(index))) {
            if (program.charAt(index) == '\n') {
                currentLine++;
            }
            index++;
        }
    }

    private void skipComments() {
        while (index < program.length() && program.charAt(index) == '#') {
            while (index < program.length() && program.charAt(index) != '\n') {
                index++;
            }
        }
    }

    private boolean treatStringConstant() {
        var regexForStringConstant = Pattern.compile("^\"([a-zA-z0-9_ ]*)\"");
        var matcher = regexForStringConstant.matcher(program.substring(index));
        if (!matcher.find()) {
            if (Pattern.compile("^\"[^\"]\"").matcher(program.substring(index)).find()) {
                throw new ScannerException("Invalid string constant at line " + currentLine);
            }
            if (Pattern.compile("^\"").matcher(program.substring(index)).find()) {
                throw new ScannerException("Missing \" at line " + currentLine);
            }
            return false;
        }
        var stringConstant = matcher.group(1);
        index += stringConstant.length() + 2;
        Pair<Integer, Integer> position = null;
        try {
            position = symbolTable.addStringConstant(stringConstant);
        } catch (Exception e) {
            throw new ScannerException(e.getMessage());
        }
        PIF.add(new ImmutablePair(PositionType.STRING_CONSTANT, position));
        return true;
    }

    private boolean treatIntConstant(){
        var regexForIntConstant = Pattern.compile("^([+-]?[1-9][0-9]*|0)");
        var matcher = regexForIntConstant.matcher(program.substring(index));
        if (!matcher.find()) {
            return false;
        }
        var intConstant = matcher.group(1);
        index += intConstant.length();
        Pair<Integer, Integer> position;
        try {
            position = symbolTable.addIntConstant(Integer.parseInt(intConstant));
        } catch (Exception e) {
            throw new ScannerException(e.getMessage());
        }
        PIF.add(new ImmutablePair(PositionType.INT_CONSTANT, position));
        return true;
    }

    private boolean treatIdentifier() {
        var regexForIdentifier = Pattern.compile("^([a-zA-Z_][a-zA-Z0-9_]*)");
        var matcher = regexForIdentifier.matcher(program.substring(index));
        if (!matcher.find()) {
            return false;
        }
        var identifier = matcher.group(1);
        index += identifier.length();
        Pair<Integer, Integer> position;
        try {
            position = symbolTable.addIdentifier(identifier);
        } catch (Exception e) {
            throw new ScannerException(e.getMessage());
        }
        PIF.add(new ImmutablePair(PositionType.IDENTIFIER, position));
        return true;
    }

    private boolean treatFromTokenList() {
        for (var token : tokens) {
            if (program.substring(index).startsWith(token)) {
                index += token.length();
                PIF.add(new ImmutablePair(tokens.indexOf(token), new ImmutablePair(-1, -1)));
                return true;
            }
        }
        return false;
    }

    private void nextToken() {
        skipSpaces();
        skipComments();
        if (index == program.length()) {
            return;
        }
        if (treatStringConstant()) {
            return;
        }
        if (treatIntConstant()) {
            return;
        }
        if (treatIdentifier()) {
            return;
        }
        if (treatFromTokenList()) {
            return;
        }
        throw new ScannerException("Invalid token at line " + currentLine);
    }

    public void scan() {
        while (index < program.length()) {
            nextToken();
        }
    }
}
