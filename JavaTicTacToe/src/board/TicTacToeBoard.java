package board;

import tictactoe.Player;

public class TicTacToeBoard extends Board<Player> {
    protected final static int DEFAULT_SIZE = 3;

    protected final int peicesToWinHorizontal;
    protected final int peicesToWinVertical;

    public TicTacToeBoard() {
        this(TicTacToeBoard.DEFAULT_SIZE, TicTacToeBoard.DEFAULT_SIZE);
    }

    public TicTacToeBoard(int width, int height) {
        this(width, height, width, height);
    }

    public TicTacToeBoard(int width, int height, int peicesToWin) {
        this(width, height, peicesToWin, peicesToWin);
    }

    protected TicTacToeBoard(int width, int height, int peicesToWinHorizontal, int peicesToWinVertical) {
        super(width, height);

        this.peicesToWinHorizontal = peicesToWinHorizontal;
        this.peicesToWinVertical = peicesToWinVertical;
    }

    public boolean isTie() {
        return super.isFull();
    }

    // abstract public boolean isPlayerWinner(Player player); 
    public boolean isPlayerWinner(Player player) {
        return false;
    } 
}