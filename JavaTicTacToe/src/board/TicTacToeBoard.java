package board;

import tictactoe.Player;

public class TicTacToeBoard extends Board<Player> {
    protected final static int DEFAULT_SIZE = 3;

    protected final int peicesToWinHorizontal;
    protected final int peicesToWinVertical;

    protected int turnCount;

    public TicTacToeBoard() {
        this(TicTacToeBoard.DEFAULT_SIZE, TicTacToeBoard.DEFAULT_SIZE);
    }

    public TicTacToeBoard(int width, int height) {
        this(width, height, width, height);
    }

    public TicTacToeBoard(int width, int height, int peicesToWinHorizontal, int peicesToWinVertical) {
        super(width, height);

        this.peicesToWinHorizontal = peicesToWinHorizontal;
        this.peicesToWinVertical = peicesToWinVertical;

        reset();
    }

    public void reset() {
        super.reset();
        this.turnCount = 0;
    }

}
