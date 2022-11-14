package tictactoe;

public class Player {
    public enum Colors {
        RESET(0),
        BLACK(30),
        RED(31),
        GREEN(32),
        YELLOW(33),
        BLUE(34),
        PURPLE(35),
        CYAN(36),
        WHITE(37);

        private final int colorCode;

        Colors(int colorCode) {
            this.colorCode = colorCode;
        }

        public String colorCode() {
            return "\u001B[" + this.colorCode + "m";
        }

        public String toString() {
            return this.colorCode();
        }
    }

    final private char letter;
    final private Colors color;

    final private int winCount;

    Player(char letter, Colors color) {
        this.letter = letter;
        this.color = color;

        this.winCount = 0;
    }

    public int getWinCount() {
        return winCount;
    }

    public int length() {
        return 1;
    }

    @Override
    public String toString() {
        return this.color + String.valueOf(this.letter) + Player.Colors.RESET;
    }
}
