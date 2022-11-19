package board;

import tictactoe.Player;

public class TicTacToeBoard extends Board<Player> {
    private final static int DEFAULT_SIZE = 3;

    private final int peicesToWinHorizontal;
    private final int peicesToWinVertical;

    private final boolean checkDiagnals;

    public TicTacToeBoard() {
        this(TicTacToeBoard.DEFAULT_SIZE, TicTacToeBoard.DEFAULT_SIZE);
    }

    /**
     * Construct a width by height board where you win by getting accros the board
     */
    public TicTacToeBoard(int width, int height) {
        this(width, height, width, height, width == height);
    }

    /**
     * Construct a width by height board where you win by getting the specified
     * number of peicesToWin in a row
     */
    public TicTacToeBoard(int width, int height, int peicesToWin) {
        this(width, height, peicesToWin, peicesToWin, true);
    }

    public TicTacToeBoard(
            int width, int height,
            int peicesToWinHorizontal, int peicesToWinVertical,
            boolean checkDiagnals) {

        super(width, height);

        this.checkDiagnals = checkDiagnals;

        this.peicesToWinHorizontal = peicesToWinHorizontal;
        this.peicesToWinVertical = peicesToWinVertical;
    }

    public boolean isTie() {
        return super.isFull();
    }

    public boolean isPlayerWinner(Player player) {
        
        if (this.checkDiagnals) {

        }
        
        return false;
    }
}