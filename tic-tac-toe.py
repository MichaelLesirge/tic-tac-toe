def main():
    print("Welcome to tic-tac-toe with python!")

    color_mode = bool_input("\u001b[31m Is this red for you \033[0m")
    # color_mode = bool_input("Does you console support ASCII color codes")
    Player.color_mode = color_mode
    print()

    if bool_input("Do you want a custom board"):
        message = "Enter the %s of the board: "
        width, height = int_input(message % "width"), int_input(message % "height")
        board = Board(width, height)
    else:
        board = Board()
    Player.board = board

    print()

    players = []
    if bool_input("Do you want a custom players"):
        for i in range(1, int_input("Enter the number of players: ") + 1):
            print()
            print(f"Player {i}")
            new_player = create_player()
            players.append(new_player)
    else:
        players.append(Player("X", "red"))
        players.append(Player("O", "blue"))

    print()

    playing = True
    while playing:
        board.new_game()
        print(f"Round {board.rounds_played}")
        while board.is_not_full():
            player = players[board.placed % len(players)]
            print(board)
            print(f"{player}'s turn.")

            player.place()

            if board.is_winner(player):
                print(board)
                player.wins += 1
                print(f"Player {player} wins!")
                break
        else:
            print(board)
            print("It's a tie!")
        print()

        for player in players:
            print(f"{player}: {player.wins}")
        print()

        playing = bool_input("Do you want to play again")

    print("Good Bye!")


class Board:
    def __init__(self, width=3, height=3):
        self.width: int = width
        self.height: int = height
        self.size: int = (self.width * self.height)

        self.rounds_played: int = 0
        self.placed: int
        self._board: dict
        self._reset()

    def new_game(self):
        self.rounds_played += 1
        self._reset()

    def _reset(self):
        self.placed = 0
        self._board = {i: str(i) for i in range(1, self.size + 1)}

    def _is_valid_location(self, loc) -> bool:
        return loc in self._board

    def _is_empty_location(self, loc) -> bool:
        return self._board[loc] == str(loc)

    def is_full(self) -> bool:
        return self.placed >= self.size

    def is_not_full(self) -> bool:
        return self.placed < self.size

    def is_winner(self, player) -> bool:
        for i in range(1, self.size + 1, self.width):
            if all(((self._board[j] == player) for j in range(i, i + self.width))):
                return True

        for i in range(1, self.width + 1):
            if all(((self._board[j] == player) for j in range(i, self.size + 1, self.width))):
                return True

        if self.width == self.height:
            if all(((self._board[i] == player) for i in range(1, self.size + 1, self.width + 1))) or \
                    all(((self._board[i] == player) for i in range(self.width, self.size, self.width - 1))):
                return True
        return False

    def __getitem__(self, item):
        return self._board[item]

    def __setitem__(self, key, value):
        self.place(key, value)

    def place(self, loc: int, val: "Player"):
        if not self._is_valid_location(loc):
            raise ValueError(f"location must be from 1 to {self.size}")
        if not self._is_empty_location(loc):
            raise ValueError("location is already occupied")
        self.placed += 1
        self._board[loc] = val

    def __repr__(self):
        return f"{self.__class__.__name__}({self._board})"

    def __str__(self):
        max_num_len = len(str(self.size))
        rows = []
        row = []
        for i in range(1, self.size + 1):
            row.append(add_buffer(self._board[i], max_num_len))
            if i % self.width == 0:
                rows.append(" " + (" | ".join(row)) + " \n")
                row = []

        line = "-" + ("-" * max_num_len) + "-"
        return "\n" + (((line + "+") * (self.width - 1)) + line + "\n").join(rows)


class Player:
    board = None
    color_mode = False

    colors = {
        "red": "\u001b[31m",
        "blue": "\u001b[34m",
        "green": "\u001b[32m",
        "yellow": "\u001b[33m",
        "magenta": "\u001b[35m",
        "cyan": "\u001b[36m",
        "white": "\u001b[37m",
    }

    def __init__(self, char: str, color: str = None):
        if len(char) != 1:
            raise ValueError("Player character must be one character")
        if not char.isalpha():
            raise ValueError("Player character must be a letter")
        self.char = char.upper()

        color = color.lower()
        if color not in Player.colors:
            raise ValueError(f"{color} is not an available color")
        self.color: str = Player.colors[color]

        self.wins = 0

    def place(self):
        while True:
            try:
                print()
                loc = input("Enter where you want to go: ")
                if not loc.isnumeric():
                    raise ValueError("Location must be a number")
                Player.board.place(int(loc), self)
                return
            except ValueError as exs:
                print_invalid(exs)

    def __repr__(self):
        return f"{self.__class__.__name__}(char={self.char}, wins={self.wins})"

    def __str__(self):
        if Player.color_mode:
            return self.color + "\033[1m" + self.char + "\033[0m"
        return self.char


def add_buffer(val, amount, *, buffer=" "):
    amount -= (1 if isinstance(val, Player) else len(val))

    side_amount, extra = divmod(amount, 2)

    return (buffer * (side_amount + extra)) + str(val) + (buffer * side_amount)


def print_invalid(exs):
    print(f"Invalid input, {exs}.")


def bool_input(prompt):
    user_input = input(prompt + " (y/n): ").strip().lower()
    if user_input in ("y", "yes", "true"):
        return True
    return False


def int_input(prompt):
    while True:
        try:
            user_input = int(input(prompt).strip())
        except ValueError:
            print_invalid("answer with a number")
        else:
            return user_input


def create_player():
    while True:
        try:
            char = input("Letter: ").strip()
            color = None
            if Player.color_mode:
                color = input("Color: ").strip()
            player = Player(char, color)
        except ValueError as exs:
            print_invalid(exs)
        else:
            return player


if __name__ == "__main__":
    main()
