package board;

import game.Player;

public class TicTacToeBoard extends Board<Player> {
    private final static int DEFAULT_SIZE = 3;

    private final Integer piecesToWinHorizontal;
    private final Integer piecesToWinVertical;
    private final Integer piecesToWinDiagonal;

    private final boolean shouldCheckHorizontal;
    private final boolean shouldCheckVertical;
    private final boolean shouldCheckDiagonal;

    public TicTacToeBoard() {
        this(TicTacToeBoard.DEFAULT_SIZE, TicTacToeBoard.DEFAULT_SIZE);
    }

    /**
     * Construct a width by height board where you win by getting across the board
     */
    public TicTacToeBoard(int width, int height) {
        // set win the amount in a row you have to get to win to the length of the row
        // only set a horizontal win condition if board is perfect square
        this(width, height, width, height, width == height ? width : null);
    }

    /**
     * Construct a width by height board where you win by getting the specified
     * number of piecesToWin in a row
     */
    public TicTacToeBoard(int width, int height, int piecesToWin) {
        this(width, height, piecesToWin, piecesToWin, piecesToWin);
    }

    /**
     * Construct a width by height board where you win by getting the specified
     * number of piecesToWin in a row for each way to win. Use negative one to make
     * it impossible
     */
    public TicTacToeBoard(
            int width, int height,
            Integer piecesToWinHorizontal, Integer piecesToWinVertical, Integer piecesToWinDiagonal) {

        super(width, height);

        this.shouldCheckHorizontal = piecesToWinHorizontal != null && piecesToWinHorizontal <= this.width;
        this.shouldCheckVertical = piecesToWinVertical != null && piecesToWinVertical <= this.height;
        this.shouldCheckDiagonal = piecesToWinDiagonal != null
                && (piecesToWinDiagonal <= this.width || piecesToWinDiagonal <= this.height);

        this.piecesToWinHorizontal = piecesToWinHorizontal;
        this.piecesToWinVertical = piecesToWinVertical;
        this.piecesToWinDiagonal = piecesToWinDiagonal;
    }

    public boolean isTie() {
        return super.isFull();
    }

    private int countSequence(int row, int col, int drow, int dcol, Object player) {
        int count = 0;
        while (isInBoard(row, col) && get(row, col) == player) {
            count += 1;
            row += drow;
            col += dcol;
        }
        return count;
    }

    private boolean checkHorizontal(Player player) {
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width - piecesToWinHorizontal + 1; col++) {
                if (countSequence(row, col, 0, 1, player) >= piecesToWinHorizontal) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean checkVertical(Player player) {
        for (int row = 0; row < height - piecesToWinVertical + 1; row++) {
            for (int col = 0; col < width; col++) {
                if (countSequence(row, col, 1, 0, player) >= piecesToWinVertical) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean checkDiagonal(Player player) {
        for (int row = 0; row < height - piecesToWinDiagonal + 1; row++) {
            for (int col = 0; col < width - piecesToWinDiagonal + 1; col++) {
                if (countSequence(row, col, 1, 1, player) >= piecesToWinDiagonal ||
                        countSequence(row, col + piecesToWinDiagonal - 1, 1, -1,
                                player) >= piecesToWinDiagonal) {
                    return true;
                }
            }
        }
        return false;
    }

    public boolean isPlayerWinner(Player player) {
        return ((shouldCheckHorizontal && checkHorizontal(player)) ||
                (shouldCheckVertical && checkVertical(player)) ||
                (shouldCheckDiagonal && checkDiagonal(player)));
    }

    // @Override
    // public String toString(int row, int col) {
    // return super.toString(row, col) + " " + "(" + row + ", " + col + ")";
    // }
}