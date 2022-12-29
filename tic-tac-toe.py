# Run here by copying and pasting code in to main file:
# https://www.programiz.com/python-programming/online-compiler/

color_mode = True

colors = {
    "red": "\u001b[31m",
    "blue": "\u001b[34m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
}

x = 2

def main() -> None:
    print("Welcome to tic-tac-toe with Python!")
    print()

    # color_mode = bool_input("Does you console support ASCII color codes if your not sure, \u001b[31mis this red for you\033[0m")

    # print()

    board = make_board()

    print()

    players = create_players()

    print()

    ties_count = 0
    game_count = 0

    playing = True
    while playing:
        board.reset()
        print(f"Round {game_count+1}")

        in_game = True
        while in_game:
            player = players[board.placed % len(players)]
            print(board)
            print(f"{player}'s turn.")

            player.take_turn(board)

            if board.is_winner(player):
                print(board)
                print(f"Player {player} wins!")
                player.wins += 1
                in_game = False
            elif board.is_full():
                print(board)
                print("It's a tie!")
                ties_count += 1
                in_game = False

        print()

        print(f"Ties: {ties_count}")
        for player in players:
            print(f"{player}: {player.wins}")
        print()

        game_count += 1

        playing = bool_input("Do you want to play again")

    print("Good Bye!")


def make_board() -> "Board":
    if bool_input("Do you want a custom board"):
        message = "Enter the %s of the board"
        width, height = int_input(message % "width", require_positive=True), int_input(
            message % "height", require_positive=True)
    else:
        width, height = Board.DEFAULT_SIZE, Board.DEFAULT_SIZE

    print()

    if bool_input("Do you want a custom win condition"):
        peices_to_win = int_input("Enter peices to win", require_positive=True)
        peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal = peices_to_win, peices_to_win, peices_to_win
    else:
        peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal = width, height, (
            width if width == height else None)

    return Board(width, height, peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal)


def create_players():
    players = []
    if bool_input("Do you want a custom players"):
        for i in range(1, int_input("Enter the number of players", require_positive=True) + 1):
            print()
            print(f"Player {i}")
            new_player = create_player()
            players.append(new_player)
    else:
        players.append(Player("X", "red"))
        players.append(Player("O", "blue"))
    return players


def create_player():
    def valid_letter(x: str) -> str:
        if len(x) != 1:
            raise ValueError("Player character must be one character")
        if not x.isalpha():
            raise ValueError("Player character must be a letter")
        return x.upper()

    def valid_color(x: str) -> str:
        x = x.lower()
        if x not in colors:
            possible_colors = list(colors.keys())
            raise ValueError(f"\"{x}\" is not an available color. Try {', '.join(possible_colors[:-1])} or {possible_colors[-1]}")
        return x

    letter = get_valid_input("Letter", valid_letter)

    color = None
    if color_mode:
        color = get_valid_input("Color", valid_color)

    return Player(letter, color)


class Board:
    DEFAULT_SIZE = 3
    OFFSET = 1

    def __init__(self, width: int, height: int, peices_to_win_horizontal: int, peices_to_win_verticle: int, peices_to_win_diagnal: int):
        self.width = width
        self.height = height

        self.dimentions = (width, height)

        self.size = (self.width * self.height)

        self.should_check_horizontal = (peices_to_win_horizontal != None) and (
            peices_to_win_horizontal <= self.width)

        self.should_check_verticle = (peices_to_win_verticle != None) and (peices_to_win_verticle <= self.height)

        self.should_check_diagonal = (peices_to_win_diagnal != None) and (peices_to_win_diagnal <= self.width or peices_to_win_diagnal <= self.height)

        self.peices_to_win_horizontal = peices_to_win_horizontal
        self.peices_to_win_verticle = peices_to_win_verticle
        self.peices_to_win_diagnal = peices_to_win_diagnal

        self.max_cell_size = len(str(self.size))

        self.placed: int
        self.board: list[list]
        self.reset()

    def reset(self):
        self.placed = 0
        self.board = [[None for col in range(self.width)]
                      for row in range(self.height)]

    def is_valid_location(self, row: int, col: int) -> bool:
        return (-1 < row < self.height) and (-1 < col < self.width)

    def is_empty_location(self, row: int, col: int) -> bool:
        return self.get(row, col) is None

    def is_full(self) -> bool:
        return self.placed >= self.size

    def win_percents(self, player: "Player") -> list[int, int, int, int]:
        win_chances = [0, 0, 0, 0]
        if self.should_check_horizontal:
            for row in range(self.height):
                count = 0
                for col in range(self.width):
                    if self.get(row, col) == player:
                        count += 1
                        if count >= self.peices_to_win_horizontal:
                            win_chances[0] = count / self.peices_to_win_horizontal
                    else:
                        count = 0

        if self.should_check_verticle:
            for col in range(self.width):
                count = 0
                for row in range(self.height):
                    if self.get(row, col) == player:
                        count += 1
                        if count >= self.peices_to_win_verticle:
                            win_chances[1] = count / self.peices_to_win_verticle
                    else:
                        count = 0

        if self.should_check_diagonal:
            isWider = self.width >= self.height
            primary = self.width if isWider else self.height
            secondary = self.width if not isWider else self.height

            for i in range(self.peices_to_win_diagnal - secondary, primary - self.peices_to_win_diagnal + 1):
                countTL2BR = 0
                countTR2BL = 0
                for j in range(secondary):
                    # top left to buttom right
                    rowTL2BR = j if isWider else i + j
                    colTL2BR = i + j if isWider else j

                    # top right to buttom left
                    rowTR2BL = j if isWider else primary - (i + j) - 1
                    colTR2BL = primary - (i + j) - 1 if isWider else j

                    # print(f'({i}, {j}) ->  tl2br:({rowTL2BR}, {colTL2BR}), tr2bl:({rowTR2BL}, {colTR2BL})')

                    if self.is_valid_location(rowTL2BR, colTL2BR):
                        if self.get(rowTL2BR, colTL2BR) == player:
                            countTL2BR += 1
                            if countTL2BR >= self.peices_to_win_diagnal:
                                win_chances[2] = countTL2BR / self.peices_to_win_diagnal
                        else:
                            countTL2BR = 0

                    if self.is_valid_location(rowTR2BL, colTR2BL):
                        if self.get(rowTR2BL, colTR2BL) == player:
                            countTR2BL += 1
                            if countTR2BL >= self.peices_to_win_diagnal:
                                win_chances[3] = countTR2BL / self.peices_to_win_diagnal
                        else:
                            countTR2BL = 0

        return win_chances

    def is_winner(self, player: "Player") -> bool:
        x = self.win_percents(player)
        return 1 in x

    def get(self, row: int, col: int):
        return self.board[row][col]

    def set(self, row: int, col: int, val) -> None:
        self.board[row][col] = val

    def place(self, loc: int, player: "Player") -> None:
        loc -= self.OFFSET

        row = loc // self.width
        col = loc - (self.width * row)

        if not self.is_valid_location(row, col):
            raise ValueError(f"location must be from 1 to {self.size}")
        if not self.is_empty_location(row, col):
            raise ValueError("location is already occupied")

        self.set(row, col, player)

        self.placed += 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.board})"

    def __str__(self) -> str:
        # I'm so sorry future self, but I realised it was possible and this project does not matter so I just did it.
        return "\n" + (("\n" + "┼".join(["─" + ("─" * self.max_cell_size) + "─"] * self.width) + "─" + "\n").join([" " + ((" " + "│" + " ").join([centered_padding(item if item is not None else str((i*self.width)+j+self.OFFSET), self.max_cell_size) for j, item in enumerate(row)]) + " ") for i, row in enumerate(self.board)])) + "\n"


class Player:
    def __init__(self, char: str, color: str = None) -> None:
        if len(char) != 1:
            raise ValueError("Player character must be one character")
        if not char.isalpha():
            raise ValueError("Player character must be a letter")
        self.char = char

        if color is not None:
            color = color.lower()
            if color not in colors:
                possible_colors = list(self.colors.keys())
                raise ValueError(
                    f"\"{color}\" is not an available color. Try {', '.join(possible_colors[:-1])} or {possible_colors[-1]}")
            color = colors[color]
        self.color = color

        self.wins = 0

    def take_turn(self, board: Board) -> None:
        while True:
            try:
                loc = int_input("Enter where you want to go")
                board.place(int(loc), self)
                return
            except ValueError as exs:
                print_invalid(exs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(char={self.char}, wins={self.wins})"

    def __str__(self) -> str:
        if color_mode and self.color:
            return self.color + "\033[1m" + self.char + "\033[0m"
        return self.char


class AI_Player(Player):
    """Very inefficent TicTacToe AI"""

    WIN_POINT_MULTIPLIER = 1
    TIE_POINT_MULTIPLIER = 0.3
    LOSE_POINT_MULTIPLIER = 0

    SAVE_FOLDER = "tic-tac-toe-AI-strategies/"
    BOARD_NAME_FORMAT = "%sx%s."

    _cached_strategies = {}

    def __init__(self, char: str, color: str = None) -> None:
        super().__init__(char, color)

    @classmethod
    def _clear_cache(cls):
        cls._cached_strategies.clear()

    @classmethod
    def train(cls, board: Board, iterations: int = 1000000) -> None:
        board_name = cls.make_board_name(board)
        stategy = {"a": "b"}
        


    @classmethod
    def make_board_name(cls, board: Board) -> str:
        return cls.BOARD_NAME_FORMAT % board.dimentions


    def take_turn(self, board: Board) -> None:
        board_name = self.make_board_name(board)
        if board_name not in self._cached_strategies:
            try:
                with open(self.SAVE_FOLDER + board_name, "r") as file:
                    self._cached_strategies[board_name] = eval(file.read)
            except FileNotFoundError as er:
                raise ValueError(f"AI_Player has not been trained on {board_name} board.") from er
            except Exception as er:
                er.add_note("Invalid file contents")
                raise er
        
        strategy = self._cached_strategies[board_name]

a = AI_Player("T")
a.take_turn(Board(3, 3, 0, 0, 0))

def centered_padding(val: str | Player, amount: int, *, buffer: str = " ") -> str:
    amount -= 1 if isinstance(val, Player) else len(val)

    side_amount, extra = divmod(amount, 2)
    return (buffer * (side_amount + extra)) + str(val) + (buffer * side_amount)


def bool_input(prompt):
    prompt += " (y/n): "
    user_input = input(prompt).strip().lower()
    return user_input in ("y", "yes", "true")

def int_input(prompt, *, require_positive=False):
    def func(x: str):
        try:
            x = int(x)
        except ValueError:
            raise ValueError("input must be number")
        if require_positive and x <= 0:
            raise ValueError("input must be positive")
        return x

    return get_valid_input(prompt, func)

def get_valid_input(prompt: str, converter, *, input_func=input):
    prompt += ": "
    while True:
        try:
            user_input = converter(input_func(prompt))
        except ValueError as er:
            print_invalid(er)
        else:
            return user_input


def print_invalid(er) -> None:
    print(f"Invalid input, {er}.")


if __name__ == "__main__":
    main()
