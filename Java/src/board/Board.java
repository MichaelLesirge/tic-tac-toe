package board;

import java.util.ArrayList;

public class Board<T> {
    private static final int locOffset = 1;

    protected final int width;
    protected final int height;

    protected final int size;

    public static final String[] boxDrawingLinesUnicode = {"│", "─", "┼"};
    public static final String[] boxDrawingLinesBasic = {"|", "-", "+"};

    private static String vertLine;
    private static String horizontalLine;
    private static String intersectionLine;

    private int itemsPlaced;

    private final ArrayList<ArrayList<T>> board;

    public Board(int width, int height) throws IllegalArgumentException {
        if (width <= 0) {
            throw new IllegalArgumentException(
                    String.format("Board width must be must be a positive number not %s.", width));
        }
        if (height <= 0) {
            throw new IllegalArgumentException(
                    String.format("Board height must be must be a positive number, not %s.", height));
        }

        this.width = width;
        this.height = height;

        this.size = this.width * this.height;

        this.board = new ArrayList<ArrayList<T>>(this.height);
        for (int i = 0; i < this.height; i++) {
            this.board.add(new ArrayList<T>());
        }

        this.reset();

        setBoardDrawingStrings(boxDrawingLinesUnicode);
    }

    public static void setBoardDrawingStrings(String[] lines) { 
        vertLine = lines[0];
        horizontalLine = lines[1];
        intersectionLine = lines[2];
    }

    public void reset() {
        for (int i = 0; i < this.height; i++) {
            this.board.get(i).clear();
            for (int j = 0; j < this.width; j++) {
                this.board.get(i).add(null);
            }
        }
        this.itemsPlaced = 0;
    }

    protected int toLoc(int i, int j) {
        return (i * this.width) + j + Board.locOffset;
    }

    protected int[] toPos(int loc) {
        loc -= Board.locOffset;
        int row = loc / this.width;
        int col = loc - (this.width * row);
        int arr[] = { row, col };
        return arr;
    }

    protected boolean isInBoard(int row, int col) {
        return ((row > -1) && (row < this.height)) && ((col > -1) && (col < this.width));
    }

    protected boolean isEmpty(int row, int col) {
        return get(row, col) == null;
    }

    protected T get(int row, int col) {
        return this.board.get(row).get(col);
    }

    protected void set(int row, int col, final T val) {
        this.board.get(row).set(col, val);
    }

    public boolean isFull() {
        return this.itemsPlaced >= this.size;
    }

    public void setTile(int loc, final T val) throws IllegalArgumentException {
        int[] pos = toPos(loc);
        int row = pos[0];
        int col = pos[1];

        if (!isInBoard(row, col)) {
            throw new IllegalArgumentException(String.format("Location %s is not in board.", loc));
        }
        if (!isEmpty(row, col)) {
            throw new IllegalArgumentException(String.format("Location %s is already taken.", loc));
        }

        this.set(row, col, val);
        this.itemsPlaced++;
    }

    public String toString(int row, int col) {
        return String.valueOf(isEmpty(row, col) ? toLoc(row, col) : get(row, col));
    }

    @Override
    public String toString() {
        String divider = " " + vertLine + " ";

        int maxValSize = 1;

        final int[][] rowsLengths = new int[this.height][this.width];
        for (int row = 0; row < height; row++) {
            final int[] rowLengths = new int[this.width];
            for (int col = 0; col < width; col++) {
                final int len = toString(row, col).replaceAll("\u001B\\[[;\\d]*m", "").length();
                maxValSize = Math.max(maxValSize, len);
                rowLengths[col] = len;
            }
            rowsLengths[row] = rowLengths;
        }

        final String[] finalRows = new String[this.height];
        for (int row = 0; row < height; row++) {
            final String[] finalRow = new String[this.width];
            for (int col = 0; col < width; col++) {
                final String val = toString(row, col);
                final int neededPadding = maxValSize - rowsLengths[row][col];
                String half = " ".repeat(Math.floorDiv(neededPadding, 2));
                String extra = ((neededPadding % 2 == 0) ? "" : " ");
                finalRow[col] = half + extra + val + half;
            }
            finalRows[row] = " " + String.join(divider, finalRow) + " ";
        }

        final String splitter = ((horizontalLine + (horizontalLine.repeat(maxValSize)) + horizontalLine)
                + intersectionLine).repeat(this.width);
        final String splitterRow = "\n" + splitter.substring(0, splitter.length() - 1) + "\n";

        return String.join(splitterRow, finalRows);
    }
}