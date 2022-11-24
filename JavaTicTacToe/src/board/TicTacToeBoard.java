package board;

import tictactoe.Player;

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

        this.shouldCheckDiagonal = peicesToWinDiagonal != null && (peicesToWinDiagonal <= this.width || peicesToWinDiagonal <= this.height);
         
        this.peicesToWinHorizontal = peicesToWinHorizontal;
        this.peicesToWinVertical = peicesToWinVertical;
        this.peicesToWinDiagonal = peicesToWinDiagonal;

        // System.out.println(this.peicesToWinHorizontal + ", " + canWinHorizontal + ", " + shouldCheckHorizontal);
    }

    public boolean isTie() {
        return super.isFull();
    }

    public boolean isPlayerWinner(Player player) {
        if (this.shouldCheckHorizontal) {
            // check horizontal
            for (int row = 0; row < this.height; row++) {
                int count = 0;
                for (int col = 0; col < this.width; col++) {
                    if (this.get(row, col) == player) {
                        if (++count >= this.peicesToWinHorizontal) return true;
                    }
                }
            }
        }

        // check verticle
        if (this.shouldCheckVertical) {
            for (int col = 0; col < this.width; col++) {
                int count = 0;
                for (int row = 0; row < this.height; row++) {
                    if (this.get(row, col) == player) {
                        if (++count >= this.peicesToWinVertical) return true;
                    }
                }
            }
        }

        if (this.shouldCheckDiagonal) {
            // top left to buttom right
            for (int i = 0; i < (this.width - this.peicesToWinDiagonal) + 1; i++) {
                int count = 0;
                for (int j = 0; j < this.height; j++) {

                    final int row = j;
                    final int col = i + j;

                    System.out.println("a: " + ("(" + i + ", " + j +  ")") + " -> " + ("(" + row + ", " + col +  ")"));

                    if (this.isInBoard(row, col)) {
                        if (this.get(row, col) == player) {
                            if (++count >= this.peicesToWinDiagonal) return true;
                        }
                    }
                }
            }

            for (int i = 1; i < (this.height - this.peicesToWinDiagonal) + 1; i++) {
                int count = 0;
                for (int j = 0; j < this.width; j++) {

                    final int row = i + j;
                    final int col = j;

                    System.out.println("b: " + ("(" + i + ", " + j +  ")") + " -> " + ("(" + row + ", " + col +  ")"));

                    if (this.isInBoard(row, col)) {
                        if (this.get(row, col) == player) {
                            if (++count >= this.peicesToWinDiagonal) return true;
                        }
                    }
                }
            }
        }

        return false;
    }

    @Override
    public String toString(int row, int col) {
        return super.toString(row, col) + " " + "(" + row + ", " + col +  ")";
    }
}