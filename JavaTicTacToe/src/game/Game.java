package game;

import board.TicTacToeBoard;

import java.util.Scanner;

public class Game {
    public static void main(String[] args) {
        final Scanner scanner = new Scanner(System.in);

        TicTacToeBoard board = null;

        final Player[] players = {
                new Player('X', Player.Colors.RED),
                new Player('O', Player.Colors.BLUE),
        };

        while (board == null) {
            final int width = getValidInt("Enter board width", scanner);
            final int height = getValidInt("Enter board height", scanner);

            final boolean customWinCondition = askYesOrNo("Add custom amount to win amount", scanner);

            try {
                if (customWinCondition) {
                    final int customWinAmount = getValidInt("Enter peices needed to win", scanner);
                    board = new TicTacToeBoard(width, height, customWinAmount);
                }
                else {
                    board = new TicTacToeBoard(width, height);
                }
            } catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            }
        }

        int ties = 0;

        boolean keepPlaying = true;
        while (keepPlaying) {

            int turnCount = 0;
            board.reset();

            boolean gameover = false;

            while (!gameover) {
                Player currentPlayer = players[turnCount % players.length];

                System.out.println("\n" + board + "\n");

                System.out.println(String.format("Turn %s, %ss go.", turnCount + 1, currentPlayer));

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

                final boolean isCurrentPlayerWinner = board.isPlayerWinner(currentPlayer);
                final boolean isTie = board.isTie();

                if (isCurrentPlayerWinner || isTie) {

                    System.out.println("\n" + board + "\n");

                    gameover = true;

                    if (isCurrentPlayerWinner) {
                        System.out.println(String.format("Player %s wins!", currentPlayer));
                        currentPlayer.addWin();
                    } else if (isTie) {
                        System.out.println("It's a tie!");
                        ties++;
                    }
                }

                turnCount++;
            }

            System.out.println();

            final String scoreFormat = "%s: %s\n";
            System.out.println("---Scores---");
            for (Player player : players) {
                System.out.printf(scoreFormat, player, player.getWinCount());
            }
            System.out.printf(scoreFormat, "Ties", ties);

            System.out.println();

            keepPlaying = askYesOrNo("Play again", scanner);
        }

        System.out.println("Goodbye!");
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

    private static boolean askYesOrNo(final String prompt, final Scanner scanner) {
        System.out.print(prompt + " [Y/n]: ");
        scanner.nextLine();

        final String input = scanner.nextLine().toLowerCase();
        return input.equals("y") || input.equals("yes");
    }
}