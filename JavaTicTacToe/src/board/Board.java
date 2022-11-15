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
            ArrayList<T> arr = new ArrayList<T>();
            for (int j = 0; j < this.width; j++) {
                arr.add(null);
            }
            this.board.add(arr);
        }

        this.reset();
    }

    protected void reset() {
        // todo this.board.forEach((el) -> Collections.fill(el, null));
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

    public boolean isBoardFull() {
        return this.placed <= this.size;
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

    @Override
    public String toString() {
        // TODO make to string method work for all values even when values (not just
        // numbers) are long.
        // Store value of longest table cell and use that instead of maxNumSize
        final int maxNumSize = String.valueOf(this.size).length();

        String spliter = "-" + "-".repeat(maxNumSize) + "-";

        String[] splitters = new String[this.width];
        for (int i = 0; i < this.width; i++) {
            splitters[i] = spliter;
        }

        final String splitterRow = String.join("+", splitters);

        String[] rows = new String[this.height];
        for (int i = 0; i < height; i++) {
            String[] row = new String[this.width];
            for (int j = 0; j < width; j++) {
                String val = String.valueOf(isEmpty(i, j) ? toLoc(i, j) : getTile(i, j));
                val += " ".repeat(Math.max(maxNumSize - val.length(), 0));
                row[j] = val;
            }

            rows[i] = " " + String.join(" | ", row);
        }
        return "\n" + String.join("\n" + splitterRow + "\n", rows) + "\n";
    }
}