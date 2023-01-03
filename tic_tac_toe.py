# Run here by copying and pasting code in to main file:
# https://www.programiz.com/python-programming/online-compiler/

from random import choices
from time import sleep, time
from abc import ABC, abstractmethod

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

OFFSET = 1

def main() -> None:
    print("Welcome to tic-tac-toe with Python!")
    print()

    # color_mode = bool_input("Does you console support ASCII color codes if your not sure, \u001b[31mis this red for you\033[0m")
    # print()

    # board = Board(3, 3, 3, 3, 3)
    board = make_board()
    print()

    # players = [Human_Player("X", "red"), AI_Player("O", "blue")]
    players = create_players()
    print()

    if any(isinstance(player, AI_Player) for player in players) and AI_Player.needs_training(board, len(players)):
        AI_Player.train(board, len(players), iterations=board.size*10000, print_percent_done=True)
        print()
    # AI_Player.train(board, len(players), iterations=10000, print_percent_done=True)

    ties_count = 0

    game_count = 0

    playing = True
    while playing:
        board.reset()
        print(f"Round {game_count+1}")

        in_game = True
        while in_game:
            current_player = players[board.placed % len(players)]
            print(board)
            print(f"{current_player}'s turn.")

            current_player.take_turn(board, len(players))

            if board.is_winner(current_player):
                print(board)
                print(f"Player {current_player} wins!")
                current_player.wins += 1
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
        width, height = int_input(message % "width", min=1), int_input(message % "height", min=1)
    else:
        width, height = Board.DEFAULT_SIZE, Board.DEFAULT_SIZE

    print()

    if bool_input("Do you want a custom win condition"):
        peices_to_win = int_input("Enter peices to win", min=1)
        peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal = peices_to_win, peices_to_win, peices_to_win
    else:
        peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal = width, height, (
            width if width == height else None)

    return Board(width, height, peices_to_win_horizontal, peices_to_win_verticle, peices_to_win_diagnal)


def create_players() -> list["Player"]:
    players = []
    if bool_input("Do you want a custom players"):
        for i in range(1, int_input("Enter the number of players", min=1) + 1):
            print()
            print(f"Player {i}")
            new_player = create_player()
            players.append(new_player)
    else:
        players.append(Human_Player("X", "red"))
        players.append(Human_Player("O", "blue"))
    return players


def create_player() -> "Player":
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

    make_ai = bool_input("Bot")

    letter = get_valid_input("Letter", valid_letter)

    color = None
    if color_mode:
        color = get_valid_input("Color", valid_color)

    player_type = AI_Player if make_ai else Human_Player

    return player_type(letter, color)


class Board:
    DEFAULT_SIZE = 3

    def __init__(self, width: int, height: int, peices_to_win_horizontal: int, peices_to_win_verticle: int, peices_to_win_diagnal: int):
        self.width = width
        self.height = height

        self.size = self.width * self.height

        self.min_loc = OFFSET
        self.max_loc = self.size + OFFSET - 1

        self.should_check_horizontal = (peices_to_win_horizontal != None) and (peices_to_win_horizontal <= self.width)
        self.should_check_verticle = (peices_to_win_verticle != None) and (peices_to_win_verticle <= self.height)
        self.should_check_diagonal = (peices_to_win_diagnal != None) and (peices_to_win_diagnal <= self.width or peices_to_win_diagnal <= self.height)

        self.peices_to_win_horizontal = peices_to_win_horizontal
        self.peices_to_win_verticle = peices_to_win_verticle
        self.peices_to_win_diagnal = peices_to_win_diagnal

        self.max_cell_size = len(str(self.size))

        self.placed: int
        self.board: list[list[object]]
        self.reset()

    def reset(self) -> None:
        self.placed = 0
        self.board = [[None for col in range(self.width)] for row in range(self.height)]

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
                        win_chances[0] = max(count / self.peices_to_win_horizontal, win_chances[0])
                    else:
                        count = 0

        if self.should_check_verticle:
            for col in range(self.width):
                count = 0
                for row in range(self.height):
                    if self.get(row, col) == player:
                        count += 1
                        win_chances[1] = max(count / self.peices_to_win_verticle, win_chances[1])
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
                            win_chances[2] = max(countTL2BR / self.peices_to_win_diagnal, win_chances[2])
                        else:
                            countTL2BR = 0

                    if self.is_valid_location(rowTR2BL, colTR2BL):
                        if self.get(rowTR2BL, colTR2BL) == player:
                            countTR2BL += 1
                            win_chances[3] = max(countTR2BL / self.peices_to_win_diagnal, win_chances[3])
                        else:
                            countTR2BL = 0

        return win_chances

    def is_winner(self, player: object) -> bool:
        chances = self.win_percents(player)
        return 1 in chances

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

        self.color = color and colors[color]

        self.wins = 0

    @abstractmethod
    def take_turn(board: Board, player_count: int) -> None:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(char={self.char}, wins={self.wins})"

    def __str__(self) -> str:
        if color_mode and self.color:
            return self.color + "\033[1m" + self.char + "\033[0m"
        return self.char

class Human_Player(Player):
    def take_turn(self, board: Board, player_count: int) -> None:
        get_valid_input("Enter where you want to go", lambda loc: board.place(loc, self), input_func=int_input)

class AI_Player(Player):
    """
    Very inefficent TicTacToe AI.
    All it does it play a bunch of games and find the "best" move for that specific situation.
    It creates a dict for each board state it encounters and saves the move that makes it win the most as the value.

    In the future I am going to make this use a real neural network / use a libary like PyTorch or Tensorflow. For now I want to try and do it with no libaries (except random)
    """
    
    MAX_POINT_COUNT = 100

    RAND_START = True
    DELAY = 0.0

    SAVE_FILE_NAME_TEMPLATE = "strategy-%s.txt"

    # {"board name": ({location for first turn: location score, ...}, {(board state): best_move, ...}), ...}
    _cached_strategies: dict[str, tuple[dict[int, int], tuple[tuple[int]]: int]] = {}

    def __init__(self, char: str, color: str = None) -> None:
        super().__init__(char, color)

    @classmethod
    def needs_training(cls, board: Board, player_count: list[Player]) -> bool:
        name = cls.make_game_name(board, player_count)
        if name in cls._cached_strategies:
            return False
        try:
            with open(cls.SAVE_FILE_NAME_TEMPLATE % name, 'r') as file:
                file.read()
        except FileNotFoundError:
            return True
        except PermissionError:
            return True
        else:
            return False
        

    @classmethod
    def train(cls, board: Board, player_count: int, iterations: int = 1000000, print_percent_done: bool = False) -> None:
        board.reset()
        
        board_name = cls.make_game_name(board, player_count)

        percentage_notifacation_interval = iterations // 100

        strategy = {}
        
        players = [AI_Player(str(i)) for i in range(player_count)]

        if print_percent_done: 
            print("start training")
            print(f"0% Complete. Game 0 of {iterations:,}\r", end="")

        start = time()

        for i in range(1, iterations+1):
            players_moves = {player: [] for player in players}

            turn_count = 0
            playing = True

            while playing:
                current_player = players[turn_count % len(players)]
                
                def make_play(board_state):    
                    options = strategy.get(board_state)
                    
                    if options is None:
                        options = strategy[board_state] = {loc: 1 for loc in range(board.min_loc, board.max_loc+1)}

                    loc = cls.pick_empty_weighted_random_loc(board, options)
                    
                    board._place(loc, current_player)
                    players_moves[current_player].append((options, loc))
                    
                current_player.make_play_any_rotation(board, strategy, make_play)

                if board.is_winner(current_player):
                    for options, indexs in players_moves[current_player]:
                        options[indexs] += (board.size - turn_count)
                    playing = False
                elif board.is_full():
                    for moves in players_moves.values():
                        for options, indexs in moves:
                            options[indexs] += 1
                    playing = False

                turn_count += 1
            
            if print_percent_done and (i % percentage_notifacation_interval == 0):
                print(f"{(i // percentage_notifacation_interval)}% Complete. Game {i:,} of {iterations:,}\r", end="")
            board.reset()

        end = time()
        
        if print_percent_done: print(f"Training process complete. {iterations:,} games played in {int(end-start):,} seconds")

        maxed_strategy = {board_state: max(moves, key=moves.get) for board_state, moves in strategy.items()}
        first_move_strategy = strategy[players[0].get_relitive_board_state(board)]

        cls._cached_strategies[board_name] = (
            first_move_strategy,
            maxed_strategy
        )

        try:
            with open(cls.SAVE_FILE_NAME_TEMPLATE % board_name, "wt") as file:
                file.write(str(cls._cached_strategies[board_name]).replace(" ", ""))
        except PermissionError as er:
            print("Can not write strategy to file in this enviroment")         

    @classmethod 
    def make_game_name(cls, board: Board, player_count: int) -> str:
        return f"b({board.width}x{board.height})w({board.peices_to_win_horizontal},{board.peices_to_win_verticle},{board.peices_to_win_diagnal})p({player_count})"

    def take_turn(self, board: Board, players_count: int) -> None:
        board_name = self.make_game_name(board, players_count)
        if board_name not in self._cached_strategies:
            try:
                with open(self.SAVE_FILE_NAME_TEMPLATE % board_name, "rt") as file:
                    self._cached_strategies[board_name] = eval(file.read())
            except PermissionError as er:
                print("Can not read strategy from file in this enviroment. AI_Player does not have strategy in cache either.")
            except FileNotFoundError as er:
                raise ValueError(f"AI_Player has not been trained on {board_name} board.") from er
            except Exception as er:
                raise ValueError(f"Invalid file contents: {er}") from er
        
        # have more random first move to make game less repitive 
        first_move_options, strategy = self._cached_strategies[board_name]
        
        if self.RAND_START and board.placed == 0:
            loc = pick_weighted_random_value(first_move_options)
            board.place(loc, self)
        else:
            def make_play(board_state):
                loc = strategy.get(board_state)

                if loc is None:
                    # TODO pick random valid choice
                    raise NotImplementedError(f"AI Player does not know what to do on this board state")
                
                board.place(loc, self)
            self.make_play_any_rotation(board, strategy, make_play) 

        sleep(self.DELAY)
    
    def make_play_any_rotation(self, board: Board, stratagy, play_func):
        placed = False
        for i in range(2):
            for j in range(4):
                if not placed:
                    board_state = self.get_relitive_board_state(board)
                    if board_state in stratagy:
                        play_func(board_state)
                        placed = True
                board.board = rotate_90_degree(board.board)
            board.board = mirrorX(board.board)
        if not placed:
            play_func(self.get_relitive_board_state(board))

    def get_relitive_board_state(self, board: Board) -> tuple[tuple[int]]:
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

    @classmethod
    def pick_empty_weighted_random_loc(cls, board: Board, options: dict[int, int], cap=float("infinity")) -> int:
        new_stratagy = {}
        for loc, points in options.items():
            if not board.is_empty_location(*board.to_indexs(loc)):
                new_stratagy[loc] = 0
            else:
                new_stratagy[loc] = min(points, cls.MAX_POINT_COUNT)
        return pick_weighted_random_value(new_stratagy)


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


def bool_input(prompt: str) -> None:
    prompt += " (y/n): "
    user_input = input(prompt).strip().lower()
    return user_input in ("y", "yes", "true")

def input_s(prompt=""):
    return input(prompt + ": ").strip()

def int_input(prompt: str, *, min = float("-infinity"), max = float("infinity")) -> None:
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
