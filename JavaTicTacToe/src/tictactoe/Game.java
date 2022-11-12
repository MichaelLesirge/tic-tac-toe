package tictactoe;

import board.TicTacToeBoard;
import tictactoe.Player;

public class Game {
    public static void main(String[] args) {

        TicTacToeBoard board = new TicTacToeBoard(3, 3);

        final Player[] players = {
            new Player('X', Player.Colors.RED),
            new Player('O', Player.Colors.RED),
        };

        bool keepPlaying = true;

        while (keepPlaying) {

        System.out.println(board);
        
        while (true) {
            try {
                board.setTile(0, this);
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }



    }
}
