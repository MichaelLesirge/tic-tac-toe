import 'dart:ffi';
import 'dart:io';
import 'dart:math';

class Board {
  int itemsPlaced = 0;
  int maxLenItem = 0;

  final int width;
  final int height;
  final List<List<String?>> board;

  Board(this.width, this.height) : this.board = List.generate(height, (_) => List<String?>.filled(width, null), growable: false) {}

  void reset() {
    maxLenItem = 0;
    itemsPlaced = 0;
    board.forEach((row) => row.fillRange(0, row.length, null));
  }

  bool isFull() {
    return itemsPlaced > width * height;
  }

  void place(int row, int col, final String item) {
    row += height - col;
    col -= 1;

    if (row < 0 || row >= height || col < 0 || col >= width)
      throw Exception("Invalid Location. Location is not in board.");

    if (board[row][col] != null)
      throw Exception("Invalid Location. Location is already occupied.");

    board[row][col] = item;

    itemsPlaced++;
    maxLenItem = max(item.length, maxLenItem);
  }

  @override
  String toString() {
    const String cross = "┼", horizontalLine = "─", verticalLine = "│";

    final int maxRowLabel = height.toString().length;
    final int itemSize = max(max(maxLenItem, maxRowLabel), 1);

    final String horizontalSep = " " + verticalLine + " ";
    final String verticalSectionSep = horizontalLine * (itemSize + horizontalSep.length - 1);
    final String verticalRowSep =  List.filled(width, verticalSectionSep).join(cross);

    final String lastLineIndex = List.generate(width, (index) => centerStr((index + 1).toString(), itemSize + horizontalSep.length - 1)).join(" " * verticalLine.length);

    StringBuffer output = StringBuffer();

    for (final (rowIndex, row) in board.indexed) {
      output.write((rowIndex + 1).toString().padRight(maxRowLabel));
      output.write(
        " " + row.map((item) => centerStr(item ?? "", itemSize)).join(horizontalSep)
      );
      output.write("\n" + (" " * (maxRowLabel)) + (rowIndex == height - 1 ? lastLineIndex : verticalRowSep) + "\n");
    }

    return output.toString();
  }
}

void main() {
  final int width = int_input("width");
  final int height = int_input("height");

  final Board board = Board(width, height);

  final String defaultPlayers = "X, O";

  final String userPlays = input("What players do you want (default ${defaultPlayers})");
  final List<String> players = (userPlays.length == 0 ? defaultPlayers : userPlays)
    .split(",")
    .map((e) => e.trim().toUpperCase())
    .toList();

  bool going = true;
  int gameNumber = 0;

  print(board);

  while (going) {
    int turnNumber = 0;

    String? winner = null;

    while (board.isFull() && winner == null) {
      String currentPlayer = players[(turnNumber + gameNumber) % players.length];

      turnNumber++;
    }

    gameNumber++;
  }
}

String centerStr(String s, int width, {String buffer = " "}) {
    final int extra_len = width - s.length;
    if (extra_len < 1) return s;
    final int side_amount = extra_len ~/ 2;
    final int extra = extra_len % 2;
    return (buffer * (side_amount + extra)) + s + (buffer * side_amount);
}

int int_input(String prompt, {String promptPostfix = ": ", String errorMessage = "Invalid number"}) {
  int? output = null;
  while (output == null) {
    try {
      output = int.parse(input(prompt, promptPostfix: promptPostfix));
    } catch (e) {
      print(errorMessage);
    }
  }
  return output;
}

String input(String prompt, {String promptPostfix = ": "}) {
  stdout.write(prompt + promptPostfix);
  String? output = stdin.readLineSync();
  return output ?? "";
}