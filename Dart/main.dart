import 'dart:io';

class Board {
  int itemsPlaced = 0;
  int maxLenItem = 0;

  final int width;
  final int height;
  final List<List<String?>> board;

  // named constructor
  Board.fromArray(this.board) : height = board.length, width = board[0].length;

  // named redirect constructor
  Board.fromSize(int size) : this(size, size);

  // main constrictor, I really like the way you can do this.attribute in constructor arguments so you don't have to manually set them 
  Board(this.width, this.height) : this.board = List.generate(height, (_) => List<String?>.filled(width, null), growable: false) {}

  void reset() {
    maxLenItem = 0;
    itemsPlaced = 0;
    board.forEach((row) => row.fillRange(0, row.length, null));
  }

  bool isFull() {
    return itemsPlaced >= size;
  }

  bool isInBoard(final int row, final int col) {
    return row > -1 && row < height && col > -1 && col < width;
  }

  int xToCol(final int x) => x - 1;
  int yToRow(final int y) => height - y;
  
  int colToX(final int col) => col + 1;
  int rowToY(final int row) => height - row;

  // getters
  int get size => width * height;

  bool isEmptyLocation(final int row, final int col) {
    return board[row][col] == null;
  }

  void place(final int x, final int y, final String item) {
    final int row = yToRow(y);
    final int col = xToCol(x);

    if (!isInBoard(row, col))
      throw "Invalid Location, location is not in board.";

    if (!isEmptyLocation(row, col))
      throw "Invalid Location, location is already occupied.";

    board[row][col] = item;

    itemsPlaced++;
    maxLenItem = max([item.length, maxLenItem]);
  }

  int countDirection(final String item, int row, int col, final int drow, final int dcol) {
    int count = 0;
    while (isInBoard(row, col) && board[row][col] == item) {
      count++;
      row += drow;
      col += dcol;
    }
    return count;
  }

  bool isWinner(String item) {
    for (int row = 0; row < height; row++) {
      if (countDirection(item, row, 0, 0, 1) >= width) return true;
    }
    for (int col = 0; col < width; col++) {
      if (countDirection(item, 0, col, 1, 0) >= height) return true;
    }
    if (width == height) {
      if (countDirection(item, 0, 0, 1, 1) >= width || countDirection(item, 0, width-1, 1, -1) >= width) return true;
    }
    return false;
  }

  @override
  String toString() {
    const String cross = "┼", horizontalLine = "─", verticalLine = "│";

    final int maxRowLabelLen = height.toString().length;
    final int itemSize = max([maxLenItem, maxRowLabelLen, 1]);

    final String horizontalSep = " " + verticalLine + " ";
    final String verticalSectionSep = horizontalLine * (itemSize + horizontalSep.length - 1);
    final String verticalRowSep =  List.filled(width, verticalSectionSep).join(cross);

    final String lastLineIndex = List.generate(width, (colIndex) => 
      centerStr(colToX(colIndex).toString(), itemSize + horizontalSep.length - 1))
    .join(" " * verticalLine.length);

    StringBuffer output = StringBuffer();

    for (final (rowIndex, row) in board.indexed) {
      output.write(rowToY(rowIndex).toString().padRight(maxRowLabelLen));
      output.write(
        " " + row.map((item) => centerStr(item ?? "", itemSize)).join(horizontalSep)
      );
      output.write("\n" + (" " * (maxRowLabelLen)) + (rowIndex == height - 1 ? lastLineIndex : verticalRowSep) + "\n");
    }

    return output.toString();
  }
}

void main() {
  final int width = intInput("width", defaultValue: 3, min: 1, errorMessage: "Invalid input, must be a positive number");
  final int height = intInput("height", defaultValue: 3, min: 1);

  final Board board = Board(width, height);

  final List<String> players = listInput("What players do you want", (e) => e.trim().toUpperCase(), defaultValue: "X, O", minLen: 1);

  bool going = true;
  int gameNumber = 0;

  final Map<String?, int> scores = Map.fromIterable([...players, null], value: (_) => 0);

  while (going) {
    int turnNumber = 0;

    String? winner = null;

    while (!board.isFull() && winner == null) {
      print("\x1B[2J\x1B[0;0H");

      String currentPlayer = players[(turnNumber + gameNumber) % players.length];

      print("${board}\n");
      print("${currentPlayer}'s turn");

      bool needsToPlace = true;

      while (needsToPlace) {
        final List<int> location = listInput("Where do you want to go", int.parse, len: 2, errorMessage: "Invalid input, must x, y number pair. Example \"1, 2\".");

        try {
          final int x = location[0], y = location[1];
          board.place(x, y, currentPlayer);       
          needsToPlace = false;
        } catch (e) {
          print(e);
        }
      }

      if (board.isWinner(currentPlayer)) {
        winner = currentPlayer;
      }

      turnNumber++;
    }

    print("\x1B[2J\x1B[0;0H");
    print(board);

    scores[winner] = scores[winner]! + 1;

    print("\nScores");
    for (final item in scores.entries) {
      print("${item.key ?? "Ties"}: ${item.value}");
    }
    print("");

    board.reset();
    gameNumber++;

    going = boolInput("Do you want to play again", defaultValue: true);
  }

}

String centerStr(String s, int width, {String buffer = " "}) {
    final int extraLen = width - s.length;
    if (extraLen < 1) return s;
    final int sideAmount = extraLen ~/ 2;
    final int extra = extraLen % 2;
    return (buffer * (sideAmount + extra)) + s + (buffer * sideAmount);
}

int max(Iterable<int> values) {
  return values.reduce((current, next) => current > next ? current : next);
}

// All of this just go get valid user input \/

bool boolInput(String prompt, {bool? defaultValue}) {
    return validInput(prompt, (source) {
      source = source.toLowerCase().trim();
      if (["y", "yes", "true"].contains(source)) return true;
      if (["n", "no", "false"].contains(source)) return false;
      if (defaultValue != null) return defaultValue;
      throw "Invalid input, Must be yes or no.";
    }, promptPostfix: " (${defaultValue == true ? "Y" : "y"}/${defaultValue == false ? "N" : "n"})? ");
}

int intInput(String prompt, {int? min, int? max, int? defaultValue, String promptPostfix = ": ", String? errorMessage = "Invalid input, must be number"}) {
  return validInput(prompt, (source) {
    final num = int.parse(source);
    if (min != null && num < min) throw "Must be greater or equal to than ${min}";
    if (max != null && num >= max) throw "Must have less than ${max}";
    return num;
  },
  defaultValue: defaultValue.toString(), promptPostfix: promptPostfix, errorMessage: errorMessage);
}

// templates
List<T> listInput<T>(String prompt, T Function(String) converter, {String splitOn = r"[,\s]", int? len, int? minLen, int? maxLen,
 String? defaultValue, String promptPostfix = ": ", String? errorMessage}) {
  return validInput(prompt, (source) {
    final items = source.split(RegExp(splitOn)).where((e) => e.length > 0).map(converter).toList();
    if (len != null && items.length != len) throw "Must have ${len} values separated by \"${splitOn}\"";
    if (minLen != null && items.length < minLen) throw "Must have more than ${minLen} values separated by \"${splitOn}\"";
    if (maxLen != null && items.length >= maxLen) throw "Must have less than ${maxLen} values separated by \"${splitOn}\"";
    return items;
  },
  defaultValue: defaultValue, promptPostfix: promptPostfix, errorMessage: errorMessage);
}

T validInput<T>(String prompt, T Function(String) converter, {String? defaultValue, String promptPostfix = ": ", String? errorMessage}) {
  while (true) {
    try {
      String userInput = defaultValue == null ? 
        input(prompt, promptPostfix: promptPostfix) : 
        defaultInput(prompt, defaultValue, promptPostfix: promptPostfix);
      return converter(userInput);
    } catch (e) {
      print(errorMessage ?? e.toString());
    }
  }
}

String defaultInput(String prompt, String defaultValue, {String promptPostfix = ": ", String? defaultMessage}) {
  String userInput = input(prompt + (defaultMessage ?? " (default ${defaultValue})"), promptPostfix: promptPostfix);
  return userInput.length > 0 ? userInput : defaultValue;
}

String input(String prompt, {String promptPostfix = ": "}) {
  stdout.write(prompt + promptPostfix);
  String? output = stdin.readLineSync();
  return output ?? "";
}