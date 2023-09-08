import java.util.ArrayList;
import java.util.Scanner;

import board.TicTacToeBoard;
import game.Player;
import game.Player.Colors;

public class Main {
    public static void main(String[] args) {
        final boolean SHOULD_CLEAR_SCREEN = true;
        final boolean SHOULD_USE_COLORS = true;
        final boolean SHOULD_USE_BOX_DRAWING_CHARS = true;

        Player.setColorMode(SHOULD_USE_COLORS);

        TicTacToeBoard.setBoardDrawingStrings(SHOULD_USE_BOX_DRAWING_CHARS ? TicTacToeBoard.boxDrawingLinesBasic : TicTacToeBoard.boxDrawingLinesBasic);

        if (SHOULD_CLEAR_SCREEN) clearScreen();
            

        final Scanner scanner = new Scanner(System.in);
        
        final Colors[] colors = {Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.PURPLE, Colors.CYAN};
        final ArrayList<Player> players = new ArrayList<>();
        
        while (players.size() == 0) {
            System.out.print("Enter your players (default is X, O): ");
            final char[] userInput = scanner.nextLine().toUpperCase().toCharArray();
            if (userInput.length == 0) {
                players.add(new Player('X', colors[0]));
                players.add(new Player('O', colors[1]));
            }
            for (char c : userInput) {
                try {
                    if (c != ' ' && c != ',') {
                        players.add(new Player(c, colors[players.size() % colors.length]));
                    } 
                } catch (IllegalArgumentException e) {
                    System.out.println(e.getMessage());
                }
            }

        }

        TicTacToeBoard board = null;
        
        while (board == null) {
            final int width = getValidInt("Enter board width", TicTacToeBoard.DEFAULT_SIZE, scanner);
            if (width > 30) System.out.println("\u001B[33mWarning: Board width might be to big for console size. Line overflow may make board appear distorted.\u001B[0m");

            final int height = getValidInt("Enter board height", TicTacToeBoard.DEFAULT_SIZE, scanner);

            final int customWinAmount = getValidInt("Enter pieces needed to win", -1, "across", scanner);

            try {
                board = (customWinAmount == -1 ? new TicTacToeBoard(width, height) : new TicTacToeBoard(width, height, customWinAmount));
            } catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            }
        }

        int ties = 0;

        boolean keepPlaying = true;
        while (keepPlaying) {

            int turnCount = 0;
            board.reset();

            boolean gameOver = false;

            while (!gameOver) {
                if (SHOULD_CLEAR_SCREEN) clearScreen();

                Player currentPlayer = players.get(turnCount % players.size());

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

                    if (SHOULD_CLEAR_SCREEN) clearScreen();
                    System.out.println("\n" + board + "\n");

                    gameOver = true;

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
        Integer num = null;
        while (num == null) {
            System.out.print(prompt + ": ");
            try {
                num = scanner.nextInt();
            } catch (java.util.InputMismatchException e) {
                System.out.println("Invalid input. Must be number.");
                scanner.nextLine();
            }
        }
        return num;
    }

    private static int getValidInt(final String prompt, final int defaultValue, Scanner scanner) {
        return getValidInt(prompt, defaultValue, Integer.toString(defaultValue), scanner);
    }

    private static int getValidInt(final String prompt, final int defaultValue, final String defaultValueName, Scanner scanner) {
        Integer num = null;
        while (num == null) {
            System.out.print(prompt + " (default is " + defaultValueName + "): ");
            try {
                String userInput = scanner.nextLine();
                num = userInput.length() == 0 ? defaultValue : Integer.parseInt(userInput);
            } catch (java.lang.NumberFormatException e) {
                System.out.println("Invalid input. Must be number.");
            }
        }
        return num;
    }

    private static boolean askYesOrNo(final String prompt, final Scanner scanner) {
        System.out.print(prompt + " [Y/n]: ");
        scanner.nextLine();

        final String input = scanner.nextLine().toLowerCase();
        return !(input.equals("n") || input.equals("no") || input.equals("false"));
    }

    private static void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
}