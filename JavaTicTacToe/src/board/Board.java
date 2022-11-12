package board;

import java.util.Arrays;

public class Board<T> {
    protected final int width;
    protected final int height;

    protected final int size;

    private T [][] board;


    public Board(int width, int height) {
        this.width = width;
        this.height = height;

        this.size = this.width * this.height;
    }

    protected void reset() {
        Arrays.fill(this.board, null);
    }

    protected int toLoc(int i, int j) {
        return (i * this.height) + j;
    }

    protected boolean isInBoard(int i, int j) {
        return ((i > -1) && (i < this.width)) && ((j > -1) && (j < this.height));
    }

    protected boolean isEmpty(int i, int j) {
        return getTile(i, j) == null;
    }

    protected T getTile(int i, int j) {
        return this.board[i][j];
    }

    protected void setTile(int i, int j, final T val) {
        this.board[i][j] = val;
    }

    public void setTile(int loc, final T val) throws Exception {
        int row = loc / this.height;
        int col = loc / (row + 1);
        if (!isInBoard(row, col)) {
            throw new Exception(String.format("Location %s is not in board", val));
        }
        if (!isEmpty(row, col)) {
            throw new Exception(String.format("Location %s is already taken", val));
        }
        this.setTile(row, col, val);
    }

    @Override
    public String toString() {
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
                String num = String.valueOf(isEmpty(i, j) ? toLoc(i, j)+1 : getTile(i, j));
                num += " ".repeat(maxNumSize - num.length());
                row[j] = num;
            }

            rows[i] = " " + String.join(" | ", row);
        }
        return  "\n" + String.join("\n" + splitterRow + "\n", rows) + "\n";
    }
}