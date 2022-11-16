package board;

import java.util.ArrayList;

public class Board<T> {
    private static final int loc_offset = 1;

    protected final int width;
    protected final int height;

    protected final int size;

    private int placed;

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

    protected void reset() {
        for (int i = 0; i < this.height; i++) {
            this.board.get(i).clear();
            for (int j = 0; j < this.width; j++) {
                this.board.get(i).add(null);
            }
        }
        this.placed = 0;
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

    protected boolean isInBoard(int i, int j) {
        return ((i > -1) && (i < this.height)) && ((j > -1) && (j < this.width));
    }

    protected boolean isEmpty(int i, int j) {
        return getTile(i, j) == null;
    }

    protected T getTile(int i, int j) {
        return this.board.get(i).get(j);
    }

    protected void setTile(int i, int j, final T val) {
        this.board.get(i).set(j, val);
    }

    protected int getPlaced() {
        return this.placed;
    }

    public boolean isFull() {
        return this.placed >= this.size;
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

        this.setTile(row, col, val);
        this.placed++;
    }

    private String getSringValueElseLoc(int i, int j) {
        return String.valueOf(isEmpty(i, j) ? toLoc(i, j) : getTile(i, j));
    }

    @Override
    public String toString() {
        String divider = " | ";

        int maxValSize = 1;

        final int[][] rows_lengths = new int[this.height][this.width];
        for (int i = 0; i < height; i++) {
            final int[] row_lengths = new int[this.width];
            for (int j = 0; j < width; j++) {
                final int len = getSringValueElseLoc(i, j).replaceAll("\u001B\\[[;\\d]*m", "").length();;
                maxValSize = Math.max(maxValSize, len); 
                row_lengths[j] = len;
            }
            rows_lengths[i] = row_lengths;
        }

        final String[] final_rows = new String[this.height];
        for (int i = 0; i < height; i++) {
            final String[] final_row = new String[this.width];
            for (int j = 0; j < width; j++) {
                final String val = getSringValueElseLoc(i, j);
                final int needed_padding = maxValSize - rows_lengths[i][j];
                String half = " ".repeat(Math.floorDiv(needed_padding, 2));
                String extra = ((needed_padding % 2 == 0) ? "" : " ");
                final_row[j] = half + val + half + extra;
            }
            final_rows[i] = " " + String.join(divider, final_row) + " ";
        }

        final String spliter = (("-" + ("-".repeat(maxValSize)) + "-") + "+").repeat(this.width);
        final String spliterRow = "\n" + spliter.substring(0, spliter.length()-1) + "\n";

        return String.join(spliterRow, final_rows);
    }
}