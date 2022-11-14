package tictactoe;

import board.TicTacToeBoard;

import java.util.Scanner;

public class Game {
    public static void main(String[] args) {
        final Scanner scanner = new Scanner(System.in);

        TicTacToeBoard board;
        do {
            System.out.print("Enter board width: ");
            int width = scanner.nextInt();
            System.out.print("Enter board height: ");
            int height = scanner.nextInt();
            try {
                board = new TicTacToeBoard(width, height);
                break;
            }
            catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            }
            
        } while (true);

        final Player[] players = {
                new Player('X', Player.Colors.RED),
                new Player('O', Player.Colors.BLUE),
        };

        boolean keepPlaying = true;

        while (keepPlaying) {

            boolean gameover = false;
            int turnCount = 0;


            while (!gameover) {
                Player currentPlayer = players[turnCount % players.length];

                System.out.println(board);

                while (true) {
                    System.out.print("Where do you want to go: ");
                    int loc = scanner.nextInt();
                    try {
                        board.setTile(loc, currentPlayer);
                        break;
                    } catch (IllegalArgumentException e) {
                        System.out.println(e.getMessage());
                    }
                }

                turnCount++;
            }

        }

        scanner.close();
    }
}
