package board;

import java.util.ArrayList;

public class Board<T> {
    private static final int loc_offset = 1;

    protected final int width;
    protected final int height;

    protected final int size;

    private int itemsPlaced;

    private final ArrayList<ArrayList<T>> board;

    public Board(int width, int height) throws IllegalArgumentException {
        if (width <= 0) {
            throw new IllegalArgumentException(
                    String.format("Board width must be must be a positive number not %s", width));
        }
        if (height <= 0) {
            throw new IllegalArgumentException(
                    String.format("Board height must be must be a positive number, not %s", height));
        }

        this.width = width;
        this.height = height;

        this.size = this.width * this.height;

        this.board = new ArrayList<ArrayList<T>>(this.height);
        for (int i = 0; i < this.height; i++) {
            this.board.add(new ArrayList<T>());
        }

        this.reset();
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
        return (i * this.width) + j + Board.loc_offset;
    }

    protected int[] toPos(int loc) {
        loc -= Board.loc_offset;
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

    protected int getItemsPlaced() {
        return this.itemsPlaced;
    }

    public boolean isFull() {
        return this.itemsPlaced >= this.size;
    }

    public void setTile(int loc, final T val) throws IllegalArgumentException {
        int[] pos = toPos(loc);
        int row = pos[0];
        int col = pos[1];

        if (!isInBoard(row, col)) {
            throw new IllegalArgumentException(String.format("Location %s is not in board", loc));
        }
        if (!isEmpty(row, col)) {
            throw new IllegalArgumentException(String.format("Location %s is already taken", loc));
        }

        this.set(row, col, val);
        this.itemsPlaced++;
    }

    private String toString(int row, int col) {
        return String.valueOf(isEmpty(row, col) ? toLoc(row, col) : get(row, col));
    }

    @Override
    public String toString() {
        String divider = " | ";

        int maxValSize = 1;

        final int[][] rows_lengths = new int[this.height][this.width];
        for (int row = 0; row < height; row++) {
            final int[] row_lengths = new int[this.width];
            for (int col = 0; col < width; col++) {
                final int len = toString(row, col).replaceAll("\u001B\\[[;\\d]*m", "").length();
                ;
                maxValSize = Math.max(maxValSize, len);
                row_lengths[col] = len;
            }
            rows_lengths[row] = row_lengths;
        }

        final String[] final_rows = new String[this.height];
        for (int row = 0; row < height; row++) {
            final String[] final_row = new String[this.width];
            for (int col = 0; col < width; col++) {
                final String val = toString(row, col);
                final int needed_padding = maxValSize - rows_lengths[row][col];
                String half = " ".repeat(Math.floorDiv(needed_padding, 2));
                String extra = ((needed_padding % 2 == 0) ? "" : " ");
                final_row[col] = half + val + half + extra;
            }
            final_rows[row] = " " + String.join(divider, final_row) + " ";
        }

        final String spliter = (("-" + ("-".repeat(maxValSize)) + "-") + "+").repeat(this.width);
        final String spliterRow = "\n" + spliter.substring(0, spliter.length() - 1) + "\n";

        return String.join(spliterRow, final_rows);
    }
}