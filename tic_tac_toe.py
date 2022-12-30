# Run here by copying and pasting code in to main file:
# https://www.programiz.com/python-programming/online-compiler/

from random import choices

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
"""
TODO right now the plan is for all players so it does not defend right
also test rotion and other stuff
"""

def main() -> None:
    print("Welcome to tic-tac-toe with Python!")
    print()

    # color_mode = bool_input("Does you console support ASCII color codes if your not sure, \u001b[31mis this red for you\033[0m")
    # print()

    
    board = Board(3, 3, 3, 3, 3)
    # board = make_board()
    # print()

    players = [Player("X", "red"), AI_Player("O", "blue")]
    # players = create_players()
    # print()

    AI_Player.train(board, players, iterations=1000000, print_percent_done=True)
    print(AI_Player._cached_strategies)

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


def create_players() -> list["Player"]:
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

    letter = get_valid_input("Letter", valid_letter)

    color = None
    if color_mode:
        color = get_valid_input("Color", valid_color)

    return Player(letter, color)


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

    def get_board_state(self) -> tuple[tuple[object]]:
        return tuple(tuple(item and item.item_count for item in row) for row in self.board)

    def to_pos(self, loc: int) -> tuple[int, int]:
        loc -= OFFSET

        row = loc // self.width
        col = loc - (self.width * row)
        return row, col

    def to_loc(self, row: int, col: int) -> int:
        return (row*self.width)+col+OFFSET

    def place(self, loc: int, player: object) -> None:
        row, col = self.to_pos(loc)

        if not self.is_valid_location(row, col):
            raise ValueError(f"location must be from 1 to {self.size}")
        if not self.is_empty_location(row, col):
            raise ValueError("location is already occupied")

        self.set(row, col, player)

        self.placed += 1

    # def __repr__(self) -> str:
    #     return f"{self.__class__.__name__}({self.board})"
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.width}, {self.height}, {self.peices_to_win_horizontal}, {self.peices_to_win_verticle}, {self.peices_to_win_diagnal})"

    def __str__(self) -> str:
        # I'm so sorry future self, but I realised it was possible and this project does not matter so I just did it.
        return "\n" + (("\n" + "┼".join(["─" + ("─" * self.max_cell_size) + "─"] * self.width) + "─" + "\n").join([" " + ((" " + "│" + " ").join([centered_padding(item if item is not None else str(self.to_loc(i, j)), self.max_cell_size) for j, item in enumerate(row)]) + " ") for i, row in enumerate(self.board)])) + "\n"


class Player:
    cur_count = 0

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
                raise ValueError(f"\"{color}\" is not an available color. Try {', '.join(possible_colors[:-1])} or {possible_colors[-1]}")
            color = colors[color]
        self.color = color

        self.item_count = self.cur_count
        Player.cur_count += 1

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
    """
    Very inefficent TicTacToe AI.
    All it does it play a bunch of games and find the "best" move for that specific situation.
    It creates a dict for each board state it encounters and saves the move that makes it win the most as the value.

    In the future I am going to make this use a real neural network / use a libary like PyTorch or Tensorflow. For now I want to try and do it with no libaries (except random)
    """

    WIN_POINT = 1
    TIE_POINT = 0.5
    MAX_POINT_COUNT = 10

    SAVE_FILE = "tic-tac-toe-AI-strategy-%s.txt"

    # {"board name": ({location for first turn: location score, ...}, {(board state with True for self and False for enemy): int, ...}), ...}
    _cached_strategies: dict[str, tuple[dict[tuple[int, int], int], dict[tuple[bool,], int]]] = {}

    def __init__(self, char: str, color: str = None) -> None:
        super().__init__(char, color)

    @classmethod
    def train(cls, board: Board, players: list[Player], iterations: int = 1000000, print_percent_done: bool = False) -> None:

        board.reset()
        
        def pick_empty_weighted_random_loc(d: dict[tuple[int, int], int], board: Board) -> tuple[int, int]:
            d1 = {}
            for (row, col), points in d.items():
                if not board.is_empty_location(row, col):
                    d1[(row, col)] = 0
                else:
                    d1[((row, col))] = min(points, cls.MAX_POINT_COUNT)
            return pick_weighted_random_value(d1)

        board_name = cls.make_board_name(board)

        percentage_notifacation_interval = iterations // 100

        strategy: dict[tuple[bool,]: dict[tuple[int, int]: int]] = {}

        if print_percent_done: print("start training")

        for i in range(1, iterations+1):
            players_moves: dict[str, list[tuple[dict[tuple[int, int], int], ]]] = {player: [] for player in players}

            turn_count = 0
            playing = True

            while playing:
                current_player = players[turn_count % len(players)]

                board_state = board.get_board_state()
                plan = get_matching_any_rotation(board_state, strategy)

                if plan is None:
                    plan = strategy[board_state] = {(row, col): 1 for col in range(board.width) for row in range(board.height)}

                try:
                    loc = pick_empty_weighted_random_loc(plan, board)
                except ValueError:
                    for moves in players_moves.values():
                        for plan, loc in moves:
                            plan[loc] += cls.TIE_POINT
                        playing = False
                else:
                    row, col = loc

                    board.set(row, col, current_player)
                    players_moves[current_player].append((plan, (row, col)))

                    if board.is_winner(current_player):
                        for plan, loc in players_moves[current_player]:
                            plan[loc] += cls.WIN_POINT
                        playing = False
                    
                    turn_count += 1
            
            if print_percent_done and (i % percentage_notifacation_interval == 0): print(f"{(i // percentage_notifacation_interval)}% Complete. (game #{i:,})")
            board.reset()

        if print_percent_done: print("Training process complete.")
        maxed_strategy = {board_state: max(moves, key=moves.get) for board_state, moves in strategy.items()}

        cls._cached_strategies[board_name] = (
            {board.to_loc(row, col): points for ((row, col), points) in strategy[board.get_board_state()].items()},
            {board_state: (board.to_loc(row, col)) for (board_state, (row, col)) in maxed_strategy.items()}
        )

        try:
            with open(cls.SAVE_FILE % board_name, "wt") as file:
                file.write(str(cls._cached_strategies[board_name]))
        except PermissionError as er:
            print("Can not write strategy to file in this enviroment")
                

    @classmethod
    def make_board_name(cls, board: Board) -> str:
        return repr(board)

    def take_turn(self, board: Board) -> None:
        board_name = self.make_board_name(board)
        if board_name not in self._cached_strategies:
            try:
                with open(self.SAVE_FILE % board_name, "rt") as file:
                    self._cached_strategies[board_name] = eval(file.read())
            except PermissionError as er:
                print("Can not read strategy from file in this enviroment")
            except FileNotFoundError as er:
                raise ValueError(f"AI_Player has not been trained on {board_name} board.") from er
            except Exception as er:
                er.add_note(f"Invalid file contents: {er}")
                raise er
        
        # have more random first move to make game less repitive 
        first_move_options, strategy = self._cached_strategies[board_name]
        
        if board.placed == 0:
            loc = pick_weighted_random_value(first_move_options)
        else:
            print(board.get_board_state())
            loc = get_matching_any_rotation(board.get_board_state(), strategy)

        if loc is None:
            raise NotImplementedError(f"did not exspore possiblity of board {board.get_board_state()}")
            # TODO pick random valid choice

        board.place(loc, self)

def get_matching_any_rotation(key: tuple[tuple[object]], d: dict[tuple[tuple[object]]: object]) -> object:
    for i in range(4):
        if key in d:
            return d[key]
        key = rotate_90_degree(key) 
    return None


def pick_weighted_random_value(d: dict[object, int]) -> object:
    return choices(list(d.keys()), d.values())[0]

def rotate_90_degree(l: tuple[tuple[object]]) -> tuple[tuple[object]]:
    return tuple(tuple(x)[::-1] for x in zip(*l))

def centered_padding(val: str | Player, amount: int, *, buffer: str = " ") -> str:
    amount -= 1 if isinstance(val, Player) else len(val)

    side_amount, extra = divmod(amount, 2)
    return (buffer * (side_amount + extra)) + str(val) + (buffer * side_amount)


def bool_input(prompt: str) -> None:
    prompt += " (y/n): "
    user_input = input(prompt).strip().lower()
    return user_input in ("y", "yes", "true")

def int_input(prompt: str, *, require_positive: bool = False) -> None:
    def func(x: str):
        try:
            x = int(x)
        except ValueError:
            raise ValueError("input must be number")
        if require_positive and x <= 0:
            raise ValueError("input must be positive")
        return x

    return get_valid_input(prompt, func)

def get_valid_input(prompt: str, converter):
    prompt += ": "
    while True:
        try:
            user_input = converter(input(prompt).strip())
        except ValueError as er:
            print_invalid(er)
        else:
            return user_input


def print_invalid(er) -> None:
    print(f"Invalid input, {er}.")


if __name__ == "__main__":
    main()
