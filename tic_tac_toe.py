# Run here by copying and pasting code in to main file:
# https://www.programiz.com/python-programming/online-compiler/

from random import choices
from time import time
from abc import ABC, abstractmethod

STR_COLOR_CODES = {
    "red": "\u001b[31m",
    "blue": "\u001b[34m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
}
STR_BOLD_CODE = "\033[1m"
STR_RESET_CODE = "\033[0m"

OFFSET = 1

CYCLE_FIRST_PLAYER = True

color_mode = True


def main() -> None:
    print("Welcome to tic-tac-toe with Python!")
    print()

    # color_mode = bool_input("Does you console support ASCII color codes if your not sure, \u001b[31mis this red for you\033[0m")
    # print()

    board = make_tic_tac_toe_board()
    print()
    # board = Board(
    #     width=3, height=3,
    #     peices_to_win_horizontal=3, peices_to_win_verticle=3, peices_to_win_diagnal=3,
    # )

    players = make_players()
    print()
    # players = [Human_Player("X", STR_COLOR_CODES["red"]), AI_Player("O", STR_COLOR_CODES["blue"])]
    # players = [AI_Player("A", STR_COLOR_CODES["green"]), AI_Player("B", STR_COLOR_CODES["cyan"]), Human_Player("C", STR_COLOR_CODES["blue"])]

    game = Game(board, players)

    AI_Player.pull_stratagy(game)
    if any(isinstance(player, AI_Player) for player in players) and AI_Player.needs_training(game):
        AI_Player.train(game, iterations=board.size * 2000, should_print_percent_done=True)
        print()
    AI_Player.save_stratagy(game)

    # AI_Player.timed_train(game, train_time=1)

    ties_count = 0

    game_count = 0

    playing = True
    while playing:
        board.reset()
        print(f"Round {game_count+1}")

        winner = game.play(cycle_first_player=CYCLE_FIRST_PLAYER)

        print(game.board)

        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a tie!")

        print()

        print(f"Ties: {ties_count}")
        for player in players:
            print(f"{player}: {player.wins}")
        print()

        playing = bool_input("Do you want to play again")

    print("Good Bye!")


def make_tic_tac_toe_board() -> "Board":
    if bool_input("Do you want a custom board"):
        message = "Enter the %s of the board"
        width, height = int_input(message % "width", min=1), int_input(message % "height", min=1)
    else:
        width, height = Board.DEFAULT_SIZE, Board.DEFAULT_SIZE

    print()

    if bool_input("Do you want a custom win condition"):
        peices_to_win = int_input("Enter peices to win", min=1)
        peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal = peices_to_win, peices_to_win, peices_to_win
    else:
        peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal = width, height, (width if width == height else None)

    return Board(width, height, peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal)


def make_players() -> list["Player"]:
    players = []
    if bool_input("Do you want a custom players"):
        for i in range(1, int_input("Enter the number of players", min=1) + 1):
            print()
            print(f"Player {i}")
            new_player = make_player()
            players.append(new_player)
    else:
        players.append(Human_Player("X", STR_COLOR_CODES["red"]))
        players.append(AI_Player("O", STR_COLOR_CODES["blue"]))
    return players


def make_player() -> "Player":
    def valid_letter(x: str) -> str:
        if len(x) != 1:
            raise ValueError("Player character must be one character")
        if not x.isalpha():
            raise ValueError("Player character must be a letter")
        return x.upper()

    def valid_color(x: str) -> str:
        x = x.lower()
        if x not in STR_COLOR_CODES:
            possible_colors = list(STR_COLOR_CODES.keys())
            raise ValueError(
                f"\"{x}\" is not an available color. Try {', '.join(possible_colors[:-1])} or {possible_colors[-1]}")
        return STR_COLOR_CODES[x]

    make_ai = bool_input("Bot")

    letter = get_valid_input("Letter", valid_letter)

    color = None
    if color_mode:
        color = get_valid_input("Color", valid_color)

    player_type = AI_Player if make_ai else Human_Player

    return player_type(letter, color)


class Game:
    def __init__(self, board: "Board", players: list["Player"]) -> None:
        self.board = board
        self.players = players

        self.game_count = 0

    def play(self, *, cycle_first_player: bool = False, **kwargs):
        winner = None
        turn_count = 0

        while not (winner or self.board.is_tie()):
            turn_count += 1
            current_player = self.players[(
                self.board.placed + (self.game_count * cycle_first_player)) % len(self.players)]

            current_player.take_turn(self, **kwargs)

            if self.board.is_winner(current_player):
                winner = current_player

        self.game_count += 1

        for player in self.players:
            if winner is player:
                player.win(self, turn_count)
            elif winner is None:
                player.tie(self, turn_count)
            else:
                player.lose(self, turn_count)
        return winner

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.board), {repr(self.players)}})"

    def __str__(self) -> str:
        return f"b({self.board.width}x{self.board.height})w({self.board.peices_to_win_horizontal},{self.board.peices_to_win_verticle},{self.board.peices_to_win_diagnal})p({len(self.players)})"


class Board:
    DEFAULT_SIZE = 3

    def __init__(self, width: int, height: int, peices_to_win_horizontal: int, peices_to_win_verticle: int, peices_to_win_diagnal: int):
        self.width = width
        self.height = height

        self.size = self.width * self.height

        self.min_loc = OFFSET
        self.max_loc = self.size + OFFSET - 1

        self.should_check_horizontal = (peices_to_win_horizontal != None) and (
            peices_to_win_horizontal <= self.width)
        self.should_check_verticle = (peices_to_win_verticle != None) and (
            peices_to_win_verticle <= self.height)
        self.should_check_diagonal = (peices_to_win_diagnal != None) and (
            peices_to_win_diagnal <= self.width or peices_to_win_diagnal <= self.height)

        self.peices_to_win_horizontal = peices_to_win_horizontal
        self.peices_to_win_verticle = peices_to_win_verticle
        self.peices_to_win_diagnal = peices_to_win_diagnal

        self.max_cell_size = len(str(self.size))

        self.placed: int
        self.board: list[list[object]]
        self.reset()

    def reset(self) -> None:
        self.placed = 0
        self.board = [[None for col in range(self.width)]
                      for row in range(self.height)]

    def is_valid_location(self, row: int, col: int) -> bool:
        return (-1 < row < self.height) and (-1 < col < self.width)

    def is_empty_location(self, row: int, col: int) -> bool:
        return self.get(row, col) is None

    def is_tie(self) -> bool:
        return self.placed >= self.size

    def is_winner(self, player: "Player") -> list[int, int, int, int]:
        # fix code duplcation here
        if self.should_check_horizontal:
            for row in range(self.height):
                count = 0
                for col in range(self.width):
                    if self.get(row, col) == player:
                        count += 1
                        if count >= self.peices_to_win_horizontal:
                            return True
                    else:
                        count = 0

        if self.should_check_verticle:
            for col in range(self.width):
                count = 0
                for row in range(self.height):
                    if self.get(row, col) == player:
                        count += 1
                        if count >= self.peices_to_win_verticle:
                            return True
                    else:
                        count = 0

        if self.should_check_diagonal:
            isWider = self.width >= self.height
            primary = self.width if isWider else self.height
            secondary = self.width if not isWider else self.height

            for i in range(self.peices_to_win_diagnal - secondary, primary - self.peices_to_win_diagnal + 1):
                countTL2BR = 0
                countTR2BL = 0
                for j in range(max(0, -i), min(secondary, primary-i)):
                    # top left to buttom right
                    rowTL2BR = j if isWider else i + j
                    colTL2BR = i + j if isWider else j

                    # top right to buttom left
                    rowTR2BL = j if isWider else primary - (i + j) - 1
                    colTR2BL = primary - (i + j) - 1 if isWider else j

                    if self.get(rowTL2BR, colTL2BR) == player:
                        countTL2BR += 1
                        if countTL2BR >= self.peices_to_win_diagnal:
                            return True
                    else:
                        countTL2BR = 0

                    if self.get(rowTR2BL, colTR2BL) == player:
                        countTR2BL += 1
                        if countTR2BL >= self.peices_to_win_diagnal:
                            return True
                    else:
                        countTR2BL = 0

    def get(self, row: int, col: int) -> object:
        return self.board[row][col]

    def set(self, row: int, col: int, val: object) -> None:
        self.board[row][col] = val

    def to_indexs(self, loc: int) -> tuple[int, int]:
        loc -= OFFSET

        row = loc // self.width
        col = loc - (self.width * row)
        return row, col

    def to_loc(self, row: int, col: int) -> int:
        return (row*self.width)+col+OFFSET

    def _place(self, loc: int, val: object) -> None:
        self.placed += 1
        row, col = self.to_indexs(loc)
        self.board[row][col] = val

    def place(self, loc: int, player: object) -> None:
        row, col = self.to_indexs(loc)

        if not self.is_valid_location(row, col):
            raise ValueError(f"location must be from 1 to {self.size}")
        if not self.is_empty_location(row, col):
            raise ValueError("location is already occupied")

        self._place(loc, player)

    # def __repr__(self) -> str:
    #     return f"<{__name__}.{self.__class__.__name__} board={self.board}>"
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.width}, {self.height}, {self.peices_to_win_horizontal}, {self.peices_to_win_verticle}, {self.peices_to_win_diagnal})"

    def __str__(self) -> str:
        # I'm so sorry future self, but I realised it was possible and this project does not matter so I just did it.
        return "\n" + (("\n" + "┼".join(["─" + ("─" * self.max_cell_size) + "─"] * self.width) + "─" + "\n").join([" " + ((" " + "│" + " ").join([centered_padding(item if item is not None else str(self.to_loc(i, j)), self.max_cell_size) for j, item in enumerate(row)]) + " ") for i, row in enumerate(self.board)])) + "\n"


class Player(ABC):
    def __init__(self, char: str, color: str = None) -> None:
        if len(char) != 1:
            raise ValueError("Player character must be one character")
        self.char = char

        self.color = color

        self.wins = 0
        self.losses = 0
        self.ties = 0

    @abstractmethod
    def take_turn(game: Game) -> None:
        pass

    def win(self, game: Game, turns: int) -> None:
        self.wins += 1

    def lose(self, game: Game, turns: int) -> None:
        self.losses += 1

    def tie(self, game: Game, turns: int) -> None:
        self.ties += 1

    @property
    def win_loss_ratio(self) -> int:
        # counting ties as half a win and loss
        tie_amount = self.ties / 2
        return (self.wins + tie_amount) / (self.losses + tie_amount)

    @property
    def score(self) -> int:
        # calculate overall score like in soccer
        return (self.wins * 3) + self.ties

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(char={self.char}, wins={self.wins})"

    def __str__(self) -> str:
        if color_mode and self.color:
            return self.color + STR_BOLD_CODE + self.char + STR_RESET_CODE
        return self.char


class Human_Player(Player):
    def take_turn(self, game: Game) -> None:
        print(game.board)
        print(f"Player {self}'s turn")

        def make_play(loc):
            game.board.place(loc, self)

        get_valid_input("Enter where you want to go", make_play, input_func=int_input)


class AI_Player(Player):
    """
    Very inefficent TicTacToe AI.
    All it does it play a bunch of games and find the "best" move for that specific situation.
    It creates a dict for each board state it encounters and saves the move that makes it win the most as the value.

    In the future I am going to make this use a real neural network / use a libary like PyTorch or Tensorflow. For now I want to try and do it with no libaries (except random)
    """

    RAND_START = True

    SAVE_FILE_NAME_TEMPLATE = "strategy-%s.txt"

    strategies: dict[str, dict[tuple[tuple[int]], dict[int, int]]] = {}

    def __init__(self, char: str, color: str = None) -> None:
        super().__init__(char, color)
        self.recent_plays = []

    @classmethod
    def needs_training(cls, game: Game) -> bool:
        return str(game) not in cls.strategies

    @classmethod
    def pull_stratagy(cls, game: Game) -> bool:
        game_name = str(game)
        try:
            with open(cls.SAVE_FILE_NAME_TEMPLATE % game_name, "r") as file:
                # Who is this Jason fellow?
                strategy = eval(file.read())
        except (FileNotFoundError, PermissionError) as er:
            return False
        except Exception as er:
            raise ValueError(f"Invlaid file contents for save file '{cls.SAVE_FILE_NAME_TEMPLATE % game_name}'") from er

        for board_state, options in strategy.items():
            cls.strategies[board_state] = sum_dicts(options, start=cls.strategies.get(board_state, {}))
        return True

    @classmethod
    def save_stratagy(cls, game: Game) -> bool:
        game_name = str(game)
        try:
            with open(cls.SAVE_FILE_NAME_TEMPLATE % game_name, "w") as file:
                # Who is this Jason fellow?
                file.write(str(cls.strategies.get(game_name, {})).replace(" ", ""))
        except (PermissionError) as er:
            return False

        return True

    @classmethod
    def train(cls, game: Game, iterations: int = 1000000, should_print_percent_done: bool = False, print_new_percent_change_amount: int = 1) -> None:
        players = [AI_Player(player.char, player.color)
                   for player in game.players]
        board = Board(game.board.width, game.board.height, game.board.peices_to_win_horizontal,
                      game.board.peices_to_win_verticle,  game.board.peices_to_win_diagnal)

        bot_game = Game(board, players)

        if should_print_percent_done:
            print("Start training.")
            print(f"0% Complete. Game 0 of {iterations:,}\r", end="")

        last_percent_done = 0
        
        start = time()
        for i in range(1, iterations+1):
            bot_game.play(training_mode=True)
            board.reset()

            if should_print_percent_done:
                percent_done = int((i / iterations) * 100)
                if percent_done >= last_percent_done + print_new_percent_change_amount:
                    print(f"{percent_done}% Complete. Game {i:,} of {iterations:,}.\r", end="")
                    last_percent_done = percent_done
                    
        end = time()

        if should_print_percent_done:
            print()
            game_time = end-start
            print(f"Training process complete. {iterations:,} games played in {seconds_to_time(int(game_time))}.")
    
    @classmethod
    def timed_train(cls, game: Game, train_time: int = 60, should_print_percent_done: bool = False, print_new_percent_change_amount: int = 1) -> None:
        players = [AI_Player(player.char, player.color)
                   for player in game.players]
        board = Board(game.board.width, game.board.height,
                      game.board.peices_to_win_horizontal, game.board.peices_to_win_verticle,  game.board.peices_to_win_diagnal)

        bot_game = Game(board, players)
        if should_print_percent_done:
            print("Start training.")
            print(f"0% Complete. 0 games played.\r", end="")

        last_percent_done = 0
        
        start_time = time()
        end_time = start_time + train_time

        cur_time = start_time
        while cur_time < end_time:
            cur_time = time()

            if should_print_percent_done:
                percent_done = int(((cur_time - start_time) / (end_time - start_time)) * 100)
                if percent_done >= last_percent_done + print_new_percent_change_amount:
                   print(f"{percent_done}% Complete. {bot_game.game_count:,} games played.\r", end="")
                   last_percent_done = percent_done

            bot_game.play(training_mode=True)
            board.reset()


        if should_print_percent_done:
            print()
            print(f"Training process complete. {bot_game.game_count:,} games played in {seconds_to_time(train_time)}.")

    def take_turn(self, game: Game, *, training_mode=False) -> None:
        strategy = self.strategies.setdefault(str(game), {})

        def make_play(board: Board, board_state: tuple[tuple[int]]):
            # would use set defualt here but than I would have to always make fallback
            options = strategy.get(board_state)
            if options is None:
                options = strategy[board_state] = {loc: int(board.is_empty_location(*board.to_indexs(loc))) for loc in range(board.min_loc, board.max_loc+1)}

            if training_mode or (self.RAND_START and board.placed == 0):
                loc = pick_weighted_random_value(options)
            else:
                loc = max(options, key=options.get)

            self.recent_plays.append((options, loc))
            board._place(loc, self)

        self.make_play_any_rotation(game.board, strategy, make_play)

    def win(self, game: Game, turns: int) -> None:
        super().win(game, turns)
        for option, loc in self.recent_plays:
            option[loc] += (game.board.size - turns) + 1
        self.recent_plays.clear()

    def lose(self, game: Game, turns: int) -> None:
        super().lose(game, turns)
        for option, loc in self.recent_plays:
            if option[loc] > 1:
                option[loc] -= 1
        self.recent_plays.clear()

    def tie(self, game: Game, turns: int) -> None:
        super().tie(game, turns)
        for option, loc in self.recent_plays:
            option[loc] += 1
        self.recent_plays.clear()

    def make_play_any_rotation(self, board: Board, stratagy, play_func):
        # spin the board to fit than keep spinning it back to orginal
        placed = False
        for i in range(2):
            for j in range(4):
                if not placed:
                    board_state = self.get_relitive_board_state(board)
                    if board_state in stratagy:
                        play_func(board, board_state)
                        placed = True
                board.board = rotate_90_degree(board.board)
            board.board = mirrorX(board.board)
        if not placed:
            play_func(board, self.get_relitive_board_state(board))

    def get_relitive_board_state(self, board: Board) -> tuple[tuple[int]]:
        # TODO make this work relitively for different players. ex: " me | p1 | p2 " == " me | p2 | p1 "
        mapper = {self: 0}
        new_board = []
        for row in board.board:
            new_row = []
            for item in row:
                if item is not None:
                    if item not in mapper:
                        mapper[item] = len(mapper)
                    item = mapper[item]
                new_row.append(item)
            new_board.append(tuple(new_row))

        return tuple(new_board)


def seconds_to_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:d}:{minutes:02d}:{seconds:02d}"


def rotate_90_degree(l):
    return type(l)(type(l[0])(x[::-1]) for x in zip(*l))


def mirrorX(l):
    return type(l)(type(l[0])(x[::-1]) for x in l)


def pick_weighted_random_value(d: dict[object, int]) -> object:
    return choices(list(d.keys()), d.values())[0]


def centered_padding(val: str | Player, amount: int, *, buffer: str = " ") -> str:
    amount -= 1 if isinstance(val, Player) else len(val)

    side_amount, extra = divmod(amount, 2)
    return (buffer * (side_amount + extra)) + str(val) + (buffer * side_amount)


def sum_dicts(*dicts: dict[object, int], start=None) -> dict[object, int]:
    if start is None: start = {}
    for d in dicts:
        for key, value in d.items():
            start[key] = value + d.get(key, 0)
    return start

def bool_input(prompt: str) -> None:
    user_input = input_s(prompt + " (y/n)").lower()
    return user_input in ("y", "yes", "true")


def input_s(prompt=""):
    return input(prompt + ": ").strip()


def int_input(prompt: str, *, min=float("-infinity"), max=float("infinity")) -> None:
    def func(x: str):
        try:
            x = int(x)
        except ValueError:
            raise ValueError("input must be number")
        if x < min:
            raise ValueError(f"input must be greater than {min}")
        if x > max:
            raise ValueError(f"input must be smaller than {max}")
        return x

    return get_valid_input(prompt, func)


def get_valid_input(prompt: str, converter, *, input_func=input_s):
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
