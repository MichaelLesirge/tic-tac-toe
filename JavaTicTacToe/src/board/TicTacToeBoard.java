package board;

import game.Player;

public class TicTacToeBoard extends Board<Player> {
    private final static int DEFAULT_SIZE = 3;

    private final Integer peicesToWinHorizontal;
    private final Integer peicesToWinVertical;
    private final Integer peicesToWinDiagonal;

    private final boolean shouldCheckHorizontal;
    private final boolean shouldCheckVertical;
    private final boolean shouldCheckDiagonal;

    public TicTacToeBoard() {
        this(TicTacToeBoard.DEFAULT_SIZE, TicTacToeBoard.DEFAULT_SIZE);
    }

    /**
     * Construct a width by height board where you win by getting accros the board
     */
    public TicTacToeBoard(int width, int height) {
        // set win the amount in a row you have to get to win to the length of the row
        // only set a horizontal win condtion if board is perfect square
        this(width, height, width, height, width == height ? width : null);
    }

    /**
     * Construct a width by height board where you win by getting the specified
     * number of peicesToWin in a row
     */
    public TicTacToeBoard(int width, int height, int peicesToWin) {
        this(width, height, peicesToWin, peicesToWin, peicesToWin);
    }

    /**
     * Construct a width by height board where you win by getting the specified
     * number of peicesToWin in a row for each way to win. Use negitive one to make
     * it impossible
     */
    public TicTacToeBoard(
            int width, int height,
            Integer peicesToWinHorizontal, Integer peicesToWinVertical, Integer peicesToWinDiagonal) {

        super(width, height);

        this.shouldCheckHorizontal = peicesToWinHorizontal != null && peicesToWinHorizontal <= this.width;
        this.shouldCheckVertical = peicesToWinVertical != null && peicesToWinVertical <= this.height;
        this.shouldCheckDiagonal = peicesToWinDiagonal != null
                && (peicesToWinDiagonal <= this.width || peicesToWinDiagonal <= this.height);

        this.peicesToWinHorizontal = peicesToWinHorizontal;
        this.peicesToWinVertical = peicesToWinVertical;
        this.peicesToWinDiagonal = peicesToWinDiagonal;
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
            for (int col = 0; col < width - peicesToWinHorizontal + 1; col++) {
                if (countSequence(row, col, 0, 1, player) >= peicesToWinHorizontal) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean checkVertical(Player player) {
        for (int row = 0; row < height - peicesToWinVertical + 1; row++) {
            for (int col = 0; col < width; col++) {
                if (countSequence(row, col, 1, 0, player) >= peicesToWinVertical) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean checkDiagonal(Player player) {
        for (int row = 0; row < height - peicesToWinDiagonal + 1; row++) {
            for (int col = 0; col < width - peicesToWinDiagonal + 1; col++) {
                if (countSequence(row, col, 1, 1, player) >= peicesToWinDiagonal ||
                        countSequence(row, col + peicesToWinDiagonal - 1, 1, -1,
                                player) >= peicesToWinDiagonal) {
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