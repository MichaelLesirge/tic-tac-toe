# Run here by copying and pasting code in to main file:
# https://www.programiz.com/python-programming/online-compiler/

from random import choices
from time import time
from abc import ABC, abstractmethod


class Config:
    OFFSET_FOR_HUMANS = 1

    CYCLE_FIRST_PLAYER = True
    AI_PLAYER_RAND_START = True

    DEFAULT_PLAYER_CHARS = ["X", "O"]
    DEFAULT_PLAYER_COUNT = len(DEFAULT_PLAYER_CHARS)

    # ordered by chance of working with start being least likely
    BOARD_CHAR_SETS = [("┼", "─", "│"), ("+", "-", "|")]


DEFAULT_PLAYER_CHARS_ORDERED = Config.DEFAULT_PLAYER_CHARS + \
    [chr(i) for i in range(ord('A'), ord('Z')+1)
     if chr(i) not in Config.DEFAULT_PLAYER_CHARS]

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

STR_ENHANCER_CODES = list(STR_COLOR_CODES.values()) + \
    [STR_BOLD_CODE, STR_RESET_CODE]


def main() -> None:
    # hacky way to get check if terminal supports the fancy unicode characters
    printed_welcome_message = False
    used_board_char_set_index = 0
    while not printed_welcome_message:
        try:
            h_line = Config.BOARD_CHAR_SETS[used_board_char_set_index][1]
            print(h_line, "Welcome to tic-tac-toe with Python!", h_line)
        except UnicodeError as ex:
            used_board_char_set_index += 1
        else:
            printed_welcome_message = True
    Game.used_board_char_set = Config.BOARD_CHAR_SETS[used_board_char_set_index]

    print()

    Game.should_use_colors = True
    # Game.should_use_colors = bool_input("Does you console support ASCII color codes if your not sure, \u001b[31mis this red for you\033[0m")
    # print()

    board = make_tic_tac_toe_board()
    print()
    # board = Board(
    #     width=3, height=3,
    #     pieces_to_win_horizontal=3, pieces_to_win_vertical=3, pieces_to_win_diagonal=2,
    # )

    players = make_players()
    print()
    # players = [Human_Player("X", STR_COLOR_CODES["red"])]
    # players = [Human_Player("X", STR_COLOR_CODES["red"]), Human_Player("O", STR_COLOR_CODES["blue"])]
    # players = [AI_Player("A", STR_COLOR_CODES["green"]), AI_Player("B", STR_COLOR_CODES["cyan"]), Human_Player("C", STR_COLOR_CODES["blue"])]

    game = Game(board, players)

    # check if any players are AI and if there are train them
    if any(isinstance(player, AIPlayer) for player in players):
        found_strategy = AIPlayer.pull_strategy(game.id)
        if not found_strategy:
            AIPlayer.train(game, iterations=board.size * 2000,
                           should_print_percent_done=True, print_new_percent_change_amount=1)
            AIPlayer.push_local_strategy(game.id)
            print()

    # AI_Player.timed_train(game, train_time_seconds=1, should_print_percent_done=True)

    playing = True
    while playing:
        board.reset()
        print(f"Round {game.game_count+Config.OFFSET_FOR_HUMANS}")

        winner = game.play(cycle_first_player=Config.CYCLE_FIRST_PLAYER)

        print(game.board)

        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a tie!")

        print()

        # scores
        print(f"Ties: {game.tied_game_count}")
        for player in players:
            print(
                f"{player}{' (AI)' if isinstance(player, AIPlayer) else ''}: {player.wins}")
        print()

        playing = get_bool_input("Do you want to play again")

    print("Good Bye!")


def make_tic_tac_toe_board() -> "Board":
    message = "Enter the %s of the board"
    width, height = get_int_input(message % "width", min=1, default=Board.DEFAULT_SIZE), get_int_input(
        message % "height", min=1, default=Board.DEFAULT_SIZE)

    print()
    pieces_to_win = get_int_input("Enter pieces to win", min=1, default="across the board")
    if pieces_to_win == "across the board":
        pieces_to_win_horizontal, pieces_to_win_vertical, pieces_to_win_diagonal = width, height, (width if width == height else None)
    else:
        pieces_to_win_horizontal, pieces_to_win_vertical, pieces_to_win_diagonal = pieces_to_win, pieces_to_win, pieces_to_win

    return Board(width, height, pieces_to_win_horizontal, pieces_to_win_vertical, pieces_to_win_diagonal)


def make_players() -> list["Player"]:
    def get_valid_letter(x: str) -> str:
        if len(x) != 1:
            raise ValueError("Player character must be one character")
        if not x.isalpha():
            raise ValueError("Player character must be a letter")
        return x.upper()

    def get_valid_color(x: str) -> str:
        x = x.lower()
        if x not in STR_COLOR_CODES:
            possible_colors = list(STR_COLOR_CODES.keys())
            raise ValueError(f"\"{x}\" is not an available color. Try {', '.join(possible_colors[:-1])} or {possible_colors[-1]}")
        return STR_COLOR_CODES[x]

    color_key_options = list(STR_COLOR_CODES.keys())

    players = []
    for i in range(get_int_input("Enter the number of players", min=1, default=Config.DEFAULT_PLAYER_COUNT)):
        print()
        print(f"Player {i + Config.OFFSET_FOR_HUMANS}")

        make_ai = get_bool_input("Bot")

        letter = get_valid_input("Letter", get_valid_letter, default=DEFAULT_PLAYER_CHARS_ORDERED[i])

        color = None
        if Game.should_use_colors:
            color = get_valid_input("Color", get_valid_color, default=color_key_options[i])

        player_type = AIPlayer if make_ai else HumanPlayer

        players.append(player_type(letter, color))

    return players


class Game:
    used_board_char_set = Config.BOARD_CHAR_SETS[-1]
    should_use_colors = True
    
    def __init__(self, board: "Board", players: list["Player"]) -> None:
        self.board = board
        self.players = players

        self.game_count = 0

        self.tied_game_count = 0

        self.id = f"{self.board.width}_{self.board.height}_{self.board.pieces_to_win_horizontal}_{self.board.pieces_to_win_vertical}_{self.board.pieces_to_win_diagonal}_{len(self.players)}"

    def play(self, *, cycle_first_player: bool = False):
        winner = None
        turn_count = 0

        while not (winner or self.board.is_tie()):
            turn_count += 1
            current_player = self.players[(
                self.board.placed + (self.game_count * cycle_first_player)) % len(self.players)]

            current_player.take_turn(self)

            if self.board.is_winner(current_player):
                winner = current_player

        self.game_count += 1

        is_tie = winner is None

        if is_tie:
            self.tied_game_count += 1

        for player in self.players:
            if player is winner:
                player.win(self, turn_count)
            elif is_tie:
                player.tie(self, turn_count)
            else:
                player.lose(self, turn_count)

        return winner

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.board), {repr(self.players)}})"


class Board:
    DEFAULT_SIZE = 3

    def __init__(self, width: int, height: int, pieces_to_win_horizontal: int, pieces_to_win_vertical: int, pieces_to_win_diagonal: int):
        self.width = width
        self.height = height

        self.size = self.width * self.height

        self.min_loc = Config.OFFSET_FOR_HUMANS
        self.max_loc = self.size + Config.OFFSET_FOR_HUMANS - 1

        self.max_cell_len = len(str(self.max_loc))

        self.should_check_horizontal = (pieces_to_win_horizontal != None) and (
            pieces_to_win_horizontal <= self.width)
        self.should_check_vertical = (pieces_to_win_vertical != None) and (
            pieces_to_win_vertical <= self.height)
        self.should_check_diagonal = (pieces_to_win_diagonal != None) and (
            pieces_to_win_diagonal <= self.width or pieces_to_win_diagonal <= self.height)

        self.pieces_to_win_horizontal = pieces_to_win_horizontal
        self.pieces_to_win_vertical = pieces_to_win_vertical
        self.pieces_to_win_diagonal = pieces_to_win_diagonal

        self.placed: int
        self.board: list[list[Player | None]]
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

    def _count_sequence(self, row: int, col: int, drow: int, dcol: int, player) -> int:
        count = 0
        while self.is_valid_location(row, col) and self.get(row, col) == player:
            count += 1
            row += drow
            col += dcol
        return count

    def check_horizontal(self, player) -> bool:
        for row in range(self.height):
            for col in range(self.width - self.pieces_to_win_horizontal + 1):
                if self._count_sequence(row, col, 0, 1, player) >= self.pieces_to_win_horizontal:
                    return True
        return False

    def check_vertical(self, player) -> bool:
        for row in range(self.height - self.pieces_to_win_vertical + 1):
            for col in range(self.width):
                if self._count_sequence(row, col, 1, 0, player) >= self.pieces_to_win_vertical:
                    return True
        return False

    def check_diagonal(self, player) -> bool:
        for row in range(self.height - self.pieces_to_win_diagonal + 1):
            for col in range(self.width - self.pieces_to_win_diagonal + 1):
                if (self._count_sequence(row, col, 1, 1, player) >= self.pieces_to_win_diagonal or
                        self._count_sequence(row, col + self.pieces_to_win_diagonal - 1, 1, -1, player) >= self.pieces_to_win_diagonal):
                    return True
        return False

    def is_winner(self, player) -> bool:
        return ((self.should_check_horizontal and self.check_horizontal(player)) or
                (self.should_check_vertical and self.check_vertical(player)) or
                (self.should_check_diagonal and self.check_diagonal(player)))

    def get(self, row: int, col: int) -> object:
        return self.board[row][col]

    def set(self, row: int, col: int, val: object) -> None:
        self.board[row][col] = val

    def to_indexes(self, loc: int) -> tuple[int, int]:
        loc -= Config.OFFSET_FOR_HUMANS

        row = loc // self.width
        col = loc - (self.width * row)
        return row, col

    def to_loc(self, row: int, col: int) -> int:
        return (row*self.width)+col+Config.OFFSET_FOR_HUMANS

    def _place(self, row: int, col: int, val: object) -> None:
        self.placed += 1
        self.board[row][col] = val

    def place(self, loc: int, player: object) -> None:
        row, col = self.to_indexes(loc)

        self.max_cell_len = max(get_colorless_len(
            str(player)), self.max_cell_len)

        if not self.is_valid_location(row, col):
            raise ValueError(
                f"location must be from {self.min_loc} to {self.max_loc}")
        if not self.is_empty_location(row, col):
            raise ValueError("location is already occupied")

        self._place(row, col, player)

    # def __repr__(self) -> str:
    #     return f"<{__name__}.{self.__class__.__name__} board={self.board}>"
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.width}, {self.height}, {self.pieces_to_win_horizontal}, {self.pieces_to_win_vertical}, {self.pieces_to_win_diagonal})"

    def __str__(self) -> str:
        # I'm so sorry future self, but I realised it was possible and this project does not matter so I just did it.
        cross, h_line, v_line = Game.used_board_char_set
        return "\n" + (("\n" + cross.join([h_line + (h_line * self.max_cell_len) + h_line] * self.width) + h_line + "\n").join([" " + ((" " + v_line + " ").join([centered_padding(str(item if item else self.to_loc(i, j)), self.max_cell_len) for j, item in enumerate(row)]) + " ") for i, row in enumerate(self.board)])) + "\n"


class Player(ABC):
    def __init__(self, char: str, color: str = None) -> None:
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
        if Game.should_use_colors and self.color:
            return self.color + STR_BOLD_CODE + self.char + STR_RESET_CODE
        return self.char


class HumanPlayer(Player):
    def take_turn(self, game: Game) -> None:
        print(game.board)
        print(f"Player {self}'s turn")

        def make_play(loc):
            game.board.place(loc, self)

        get_valid_input("Enter where you want to go",
                        make_play, input_func=get_int_input)


class AIPlayer(Player):
    """
    Very inefficient TicTacToe AI.
    All it does it play a bunch of games and find the "best" move for that specific situation.
    It creates a dict for each board state it encounters and saves the move that makes it win the most as the value.

    In the future I am going to make this use a real neural network / use a library like PyTorch or Tensorflow. For now I want to try and do it with no libraries (except random)
    """

    SAVE_FILE_NAME_TEMPLATE = "strategy_%s.txt"

    local_strategies: dict[str, dict[tuple[tuple[int]],
                                     dict[tuple[int, int], int]]] = {}

    def __init__(self, char: str, color: str = None, *, start_in_training_mode: bool = False) -> None:
        super().__init__(char, color)
        self.recent_plays = []
        self.in_training_mode = start_in_training_mode

    @classmethod
    def pull_strategy(cls, game_id: str) -> bool:
        try:
            with open(cls.SAVE_FILE_NAME_TEMPLATE % game_id, "r") as file:
                # pulled_strategy = json.load(file)
                pulled_strategy = eval(file.read())
        except (FileNotFoundError, PermissionError) as er:
            return False
        except Exception as er:
            raise ValueError(f"Invalid file contents for save file '{cls.SAVE_FILE_NAME_TEMPLATE % game_id}'. Delete file and retrain to fix error") from er
        cls.local_strategies[game_id] = pulled_strategy
        return True

    @classmethod
    def push_local_strategy(cls, game_id: str) -> bool:
        try:
            with open(cls.SAVE_FILE_NAME_TEMPLATE % game_id, "w") as file:
                # can't store to json because tuples as dict keys is not allowed
                # json.dump(cls.local_strategies[game_id], file)
                file.write(str(cls.local_strategies[game_id]).replace(" ", ""))
        except (PermissionError) as er:
            return False

        return True

    @classmethod
    def train(cls, game: Game, iterations: int = 1000000, should_print_percent_done: bool = False, print_new_percent_change_amount: int = 1) -> None:
        bot_game = create_training_game(game)

        if should_print_percent_done:
            print("Start training.")
            print(f"0% Complete. Game 0 of {iterations:,}\r", end="")

        last_percent_done = 0

        start = time()
        for i in range(1, iterations+1):
            bot_game.play()
            bot_game.board.reset()

            if should_print_percent_done:
                percent_done = (i / iterations) * 100
                if percent_done >= last_percent_done + print_new_percent_change_amount:
                    print(
                        f"{int(percent_done)}% Complete. Game {i:,} of {iterations:,}.\r", end="")
                    last_percent_done = percent_done

        end = time()

        if should_print_percent_done:
            print(f"100% Complete. Game {i:,} of {iterations:,}.\r", end="")
            print()
            print(f"Training process complete. {iterations:,} games played in {seconds_to_time(int(end-start))}.")

    @classmethod
    def timed_train(cls, game: Game, train_time_seconds: int = 60, should_print_percent_done: bool = False, print_new_percent_change_amount: int = 1) -> None:

        bot_game = create_training_game(game)

        if should_print_percent_done:
            print("Start training.")
            print(f"0% Complete. 0 games played.\r", end="")

        last_percent_done = 0

        start_time = time()
        end_time = start_time + train_time_seconds

        cur_time = start_time
        while cur_time < end_time:
            bot_game.play()
            bot_game.board.reset()

            cur_time = time()

            if should_print_percent_done:
                percent_done = ((cur_time - start_time) /
                                train_time_seconds) * 100
                if percent_done >= last_percent_done + print_new_percent_change_amount:
                    print(
                        f"{int(percent_done)}% Complete. {bot_game.game_count:,} games played.\r", end="")
                    last_percent_done = percent_done

        if should_print_percent_done:
            print(
                f"100% Complete. {bot_game.game_count:,} games played.\r", end="")
            print()
            print(
                f"Training process complete. {bot_game.game_count:,} games played in {seconds_to_time(train_time_seconds)}.")

    def take_turn(self, game: Game) -> None:
        strategy = self.local_strategies.setdefault(game.id, {})

        def make_play(board, board_state):
            # would use set default here but than I would have to always make fallback
            # options = strategy.setdefault(board_state, {(row, col): int(board.is_empty_location(row, col)) for col in range(board.width) for row in range(board.height)})

            options = strategy.get(board_state)

            if options is None:
                options = strategy[board_state] = {(row, col): int(board.is_empty_location(row, col)) for col in range(board.width) for row in range(board.height)}

            if self.in_training_mode or (Config.AI_PLAYER_RAND_START and board.placed == 0):
                row, col = pick_weighted_random_key(options)
            else:
                row, col = max(options, key=options.get)

            self.recent_plays.append((options, (row, col)))
            board._place(row, col, self)

        self.make_play_any_rotation(game.board, strategy, make_play)

    def win(self, game: Game, turns: int) -> None:
        super().win(game, turns)
        if self.in_training_mode:
            self.reward_points_for_plays(game.board.size - turns + 1)
        self.recent_plays.clear()

    def lose(self, game: Game, turns: int) -> None:
        super().lose(game, turns)
        if self.in_training_mode:
            self.reward_points_for_plays(-1)

        self.recent_plays.clear()

    def tie(self, game: Game, turns: int) -> None:
        super().tie(game, turns)
        if self.in_training_mode:
            self.reward_points_for_plays(1)
        self.recent_plays.clear()

    def reward_points_for_plays(self, points: int) -> None:
        pos = points > -1
        for option, loc in self.recent_plays:
            if pos or option[loc] > 1:
                option[loc] += points

    def make_play_any_rotation(self, board: Board, strategy, play_func):
        # spin the board to fit than keep spinning it back to original
        placed = False
        for i in range(2):
            for j in range(4):
                if not placed:
                    board_state = self.get_relative_board_state(board)
                    if board_state in strategy:
                        play_func(board, board_state)
                        placed = True
                board.board = rotate_90_degree(board.board)
            board.board = mirror_x(board.board)
        if not placed:
            play_func(board, self.get_relative_board_state(board))

    def get_relative_board_state(self, board: Board) -> tuple[tuple[int]]:
        # TODO make this work relatively for different players. ex: " me | p1 | p2 " == " me | p2 | p1 "
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


def create_training_game(game: Game) -> Game:
    players = [AIPlayer(player.char, player.color, start_in_training_mode=True) for player in game.players]
    board = Board(game.board.width, game.board.height,
                  game.board.pieces_to_win_horizontal, game.board.pieces_to_win_vertical,  game.board.pieces_to_win_diagonal)

    return Game(board, players)


def seconds_to_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:d}:{minutes:02d}:{seconds:02d}"


def rotate_90_degree(l: list[list[object]]) -> list[list[object]]:
    return list(x[::-1] for x in zip(*l))


def mirror_x(l: list[list[object]]) -> list[list[object]]:
    return list(x[::-1] for x in l)


def pick_weighted_random_key(d: dict[object, int]) -> object:
    return choices(list(d.keys()), d.values())[0]


def get_colorless_len(s: str) -> int:
    for color_code in STR_ENHANCER_CODES:
        s = s.replace(color_code, "")
    return len(s)


def centered_padding(s: str, amount: int, *, buffer: str = " ") -> str:
    # cant use .center on string because of color codes counting in default len()
    amount -= get_colorless_len(s)

    side_amount, extra = divmod(amount, 2)
    return (buffer * (side_amount + extra)) + str(s) + (buffer * side_amount)


def input_s(prompt = "") -> str:
    return input(prompt + ": ").strip()

DEFAULT_SENTINEL = object()

def get_bool_input(prompt: str, default: bool = DEFAULT_SENTINEL) -> None:
    def func(x: str) -> bool:
        x = x.lower()
        if x in ("y", "yes", "true"):
            return True
        elif x in ("n", "no", "false"):
            return False
        raise ValueError("input must be Yes or No")

    return get_valid_input(prompt + "(y/n)", func, default = default, convert_default = False)

def get_int_input(prompt: str, *, min: int = float("-inf"), max: int = float("inf"), default: int = DEFAULT_SENTINEL) -> int:

    def func(x: str) -> int:
        try:
            x = int(x)
        except ValueError:
            raise ValueError("input must be number")
        if x < min:
            raise ValueError(f"input must be greater than {min}")
        if x > max:
            raise ValueError(f"input must be smaller than {max}")
        return x

    return get_valid_input(prompt, func, default = default, convert_default = False)


def get_valid_input(prompt: str, converter: callable, *, input_func = input_s, default = None, convert_default: bool = True):
    if default is not DEFAULT_SENTINEL:
        prompt += f" (default is {default})"

    while True:
        try:
            user_input = input_func(prompt)
            if default is not None and user_input == "":
                if convert_default:
                    return converter(default)
                else:
                    return default
            converted_user_input = converter(user_input)
        except ValueError as er:
            print_invalid(er)
        else:
            return converted_user_input


def print_invalid(er) -> None:
    print(f"Invalid input, {er}.")


if __name__ == "__main__":
    main()
