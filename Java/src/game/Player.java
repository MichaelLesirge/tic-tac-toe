package game;

public class Player {
    public static enum Colors {
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

        @Override
        public String toString() {
            return this.colorCode();
        }
    }

    static private boolean useColors = true;

    final private char letter;
    final private Colors color;

    private int winCount;

    public Player(char letter) {
        this(letter, null);
    }

    public Player(char letter, Colors color) throws IllegalArgumentException {

        if (!Character.isLetter(letter)) {
            throw new IllegalArgumentException(String.format("letter must be a letter not '%s'.", letter));
        }

        this.letter = letter;
        this.color = color;

        this.winCount = 0;
    }

    public int getWinCount() {
        return winCount;
    }

    public void addWin() {
        winCount++;
    }

    public static void setColorMode(boolean useColors) {
        Player.useColors = useColors;
    }

    @Override
    public String toString() {
        final String letter = String.valueOf(this.letter);

        if (!Player.useColors || this.color == null)
            return letter;

        final String boldCode = "\033[1m";

        return this.color + boldCode + String.valueOf(this.letter) + Player.Colors.RESET;
    }
}
