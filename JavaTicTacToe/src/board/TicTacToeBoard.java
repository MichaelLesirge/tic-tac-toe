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
                        if (++count >= this.peicesToWinHorizontal) {
                            return true;
                        }
                    }
                    else {
                        count = 0;
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
                        if (++count >= this.peicesToWinVertical) {
                            return true;
                        }
                    }
                    else {
                        count = 0;
                    }
                }
            }
        }

        if (this.shouldCheckDiagonal) {
            
            final boolean isWider = this.width >= this.height;
            
            final int primary = isWider ? this.width : this.height;
            final int secondary = !isWider ? this.width : this.height;
            
            for (int i = this.peicesToWinDiagonal-secondary; i < primary - this.peicesToWinDiagonal + 1; i++) {
                int countTL2BR = 0;
                int countTR2BL = 0;
                for (int j = 0; j < secondary; j++) {
                    
                    // top left to buttom right
                    final int rowTL2BR = isWider ? j : i+j;
                    final int colTL2BR = isWider ? i+j : j;
        
                    // top right to buttom left
                    final int rowTR2BL = isWider ? j : primary-(i+j)-1;
                    final int colTR2BL = isWider ? primary-(i+j)-1 : j;

                    // System.out.println(String.format("(%s, %s) ->  tl2br:(%s, %s), tr2bl:(%s, %s)", i, j, rowTL2BR, colTL2BR, rowTR2BL, colTR2BL));

                    if (this.isInBoard(rowTL2BR, colTL2BR)) {
                        if (this.get(rowTL2BR, colTL2BR) == player) {
                            if (++countTL2BR >= this.peicesToWinDiagonal) {
                                return true;
                            }
                        }
                        else {
                            countTL2BR = 0;
                        }
                    }
                    
                    if (this.isInBoard(rowTR2BL, colTR2BL)) {
                        if (this.get(rowTR2BL, colTR2BL) == player) {
                            if (++countTR2BL >= this.peicesToWinDiagonal) {
                                return true;
                            }
                        }
                        else {
                            countTR2BL = 0;
                        }
                    }
                }
            }
        }

        return false;
    }

    // @Override
    // public String toString(int row, int col) {
    //     return super.toString(row, col) + " " + "(" + row + ", " + col +  ")";
    // }
}