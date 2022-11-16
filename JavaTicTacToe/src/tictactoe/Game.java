package tictactoe;

import board.TicTacToeBoard;

import java.util.Scanner;

public class Game {
    public static void main(String[] args) {
        final Scanner scanner = new Scanner(System.in);

        TicTacToeBoard board = null;

        boolean needsValidBoardSizes = true;
        while (needsValidBoardSizes) {
            final int width = getValidInt("Enter board width", scanner);
            final int height = getValidInt("Enter board height", scanner);
            try {
                board = new TicTacToeBoard(width, height);
                needsValidBoardSizes = false;
            }
            catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            }
        }

        final Player[] players = {
                new Player('X', Player.Colors.RED),
                new Player('O', Player.Colors.BLUE),
        };

        int ties = 0;

        boolean keepPlaying = true;
        while (keepPlaying) {

            int turnCount = 0;
            
            boolean gameover = false;
            while (!gameover) {
                Player currentPlayer = players[turnCount % players.length];

                System.out.println("\n" + board + "\n");

                boolean needsValidLoc = true;
                while (needsValidLoc) {
                    int loc = getValidInt("Where do you want to go", scanner);
                    try {
                        board.setTile(loc, currentPlayer);
                        needsValidLoc = false;
                    } catch (IllegalArgumentException e) {
                        System.out.println(e.getMessage());
                    }
                }

                if (board.isPlayerWinner(currentPlayer)) {
                    System.out.printf("Player %s wins!", currentPlayer);
                    currentPlayer.addWin();
                    gameover = true;
                }
                else if (board.isFull()) {
                    System.out.println("It's a tie!");
                    ties++;
                    gameover = true;
                }

                turnCount++;
            }

            System.out.println("Scores:");
        }

        scanner.close();
    }

    private static int getValidInt(final String prompt, Scanner scanner) {
        int num = 0;
        boolean needsValidInput = true;
        while (needsValidInput) {
            System.out.print(prompt + ": ");
            try {
                num = scanner.nextInt();
                needsValidInput = false;
            } catch (java.util.InputMismatchException e) {
                System.out.println("Invalid input. Must be number.");
                scanner.nextLine();
            }
        }
        return num;

    }
}
