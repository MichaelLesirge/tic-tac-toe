# Run here by copying and pasting code in to main file:
# https://www.programiz.com/python-programming/online-compiler/

def main():
    print("Welcome to tic-tac-toe with python!")

    # color_mode = bool_input("Does you console support ASCII color codes if your not sure, \u001b[31mis this red for you\033[0m")
    # Player.color_mode = color_mode
    # print()

    Player.color_mode = True

    if bool_input("Do you want a custom board"):
        message = "Enter the %s of the board: "
        width, height = int_input(message % "width"), int_input(message % "height")
        board = Board(width, height)
    else:
        board = Board()
    Player.board = board

    print()

    if bool_input("Do you want a custom win condtion"):
        pass

    print()

    players: list[Player] = []
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

            player.take_turn(on=board)

            if board.is_winner(player):
                print(board)
                player.wins += 1
                print(f"Player {player} wins!")
                in_game = False
            elif board.is_full():
                print(board)
                ties_count += 1
                print("It's a tie!")
                in_game = False
        print()

        print(f"Ties: {ties_count}")
        for player in players:
            print(f"{player}: {player.wins}")
        print()

        game_count += 1

        playing = bool_input("Do you want to play again")

    print("Good Bye!")


class Board:
    DEFAULT_SIZE = 3
    OFFSET = 1

    def __init__(self, width=DEFAULT_SIZE, height=DEFAULT_SIZE):
        self.width: int = width
        self.height: int = height
        self.size: int = (self.width * self.height)

        self.placed: int
        self.board: list[list]
        self.reset()

    def reset(self):
        self.placed = 0
        self.board = [[None for col in range(self.width)]
                      for row in range(self.height)]

    def is_valid_location(self, row, col) -> bool:
        return (row < self.height) and (col < self.width)

    def is_empty_location(self, row, col) -> bool:
        return self.board[row][col] is None

    def is_full(self) -> bool:
        return self.placed >= self.size

    def is_winner(self, player) -> bool:
        # todo
        return False

    def place(self, loc: int, val: "Player"):
        loc -= self.OFFSET

        row = loc // self.width
        col = loc - (self.width * row)

        if not self.is_valid_location(row, col):
            raise ValueError(f"location must be from 1 to {self.size}")
        if not self.is_empty_location(row, col):
            raise ValueError("location is already occupied")

        self.board[row][col] = val

        self.placed += 1

    def __repr__(self):
        return f"{self.__class__.__name__}({self.board})"

    def __str__(self):
        # I'm so sorry future self, but I realised it was possible and this projected does not matter so I just did it.
        return "\n" + (("\n" + "┼".join(["-" + ("-" * len(str(self.size))) + "-"] * self.width) + "-" + "\n").join([" " + ((" " + "│" + " ").join([centered_padding(str(item if item is not None else ((i*self.width)+j+self.OFFSET)), len(str(self.size))) for j, item in enumerate(row)]) + " ") for i, row in enumerate(self.board)])) + "\n"


class Player:
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

        if (color is not None) and Player.color_mode:
            color = color.lower()
            if color not in Player.colors:
                possible_colors = list(self.colors.keys())
                raise ValueError(
                    f"\"{color}\" is not an available color. Try {', '.join(possible_colors[:-1])} or {possible_colors[-1]}")
            color = Player.colors[color]
        self.color = color

        self.wins = 0

    def take_turn(self, on: Board):
        while True:
            try:
                print()
                loc = input("Enter where you want to go: ")
                if not loc.isnumeric():
                    raise ValueError("Location must be a number")
                on.place(int(loc), self)
                return
            except ValueError as exs:
                print_invalid(exs)

    def __repr__(self):
        return f"{self.__class__.__name__}(char={self.char}, wins={self.wins})"

    def __str__(self):
        if Player.color_mode:
            return self.color + "\033[1m" + self.char + "\033[0m"
        return self.char


def centered_padding(val, amount, *, buffer=" "):
    amount -= (1 if isinstance(val, Player) else len(val))

    side_amount, extra = divmod(amount, 2)

    return (buffer * (side_amount + extra)) + str(val) + (buffer * side_amount)


def print_invalid(exs):
    print(f"Invalid input, {exs}.")


def bool_input(prompt):
    user_input = input(prompt + " (y/n): ").strip().lower()
    return user_input in ("y", "yes", "true")


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
            player = Player(char)
            break
        except ValueError as exs:
            print_invalid(exs)
    if Player.color_mode:
        while True:
            try:
                color = input("Color: ").strip().lower()
                player = Player(char, color)
                break
            except ValueError as exs:
                print_invalid(exs)
    return player


if __name__ == "__main__":
    main()
