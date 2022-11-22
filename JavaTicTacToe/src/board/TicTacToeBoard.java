package board;

import tictactoe.Player;

public class TicTacToeBoard extends Board<Player> {
    private final static int DEFAULT_SIZE = 3;

    private final int peicesToWinHorizontal;
    private final int peicesToWinVertical;
    private final int peicesToWinDiagonal;

    public TicTacToeBoard() {
        this(TicTacToeBoard.DEFAULT_SIZE, TicTacToeBoard.DEFAULT_SIZE);
    }

    /**
     * Construct a width by height board where you win by getting accros the board
     */
    public TicTacToeBoard(int width, int height) {
        this(width, height, width, height, width == height ? width : -1);
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
            int peicesToWinHorizontal, int peicesToWinVertical, int peicesToWindiagonal) {

        super(width, height);

        this.peicesToWinDiagonal = peicesToWindiagonal;
        this.peicesToWinHorizontal = peicesToWinHorizontal;
        this.peicesToWinVertical = peicesToWinVertical;
    }

    public boolean isTie() {
        return super.isFull();
    }

    public boolean isPlayerWinner(Player player) {
        // check horizontal
        if (this.peicesToWinHorizontal != -1) {
            for (int row = 0; row < this.height; row++) {
                int count = 0;
                for (int col = 0; col < this.width; col++) {
                    if (this.get(row, col) == player) {
                        count++;
                        if (count >= this.peicesToWinHorizontal) {
                            return true;
                        }
                    }
                }
            }
        }

        // check verticle
        if (this.peicesToWinVertical != -1) {
            for (int col = 0; col < this.width; col++) {
                int count = 0;
                for (int row = 0; row < this.height; row++) {
                    if (this.get(row, col) == player) {
                        count++;
                        if (count >= this.peicesToWinVertical) {
                            return true;
                        }
                    }
                }
            }
        }

        if (this.peicesToWinDiagonal != -1) {

        }

        return false;
    }
}