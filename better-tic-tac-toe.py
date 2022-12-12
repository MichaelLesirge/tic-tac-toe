from math import ceil

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def create_n_dimentional_list(dimentions: list[int], fill_factory, *, indexs = None) -> list:
    if indexs is None:
        indexs = []
    if len(dimentions) == 0:
        return fill_factory(indexs)
    return [
        create_n_dimentional_list(dimentions[1:], fill_factory, indexs = indexs + [i]) for i in range(dimentions[0])
    ]


def split_ints(s: str, seps=(",", "x")):
    final_sep = seps[-1]
    for sep in seps[:-1]:
        s = s.replace(sep, final_sep)

    return [int(val.strip()) for val in s.split(final_sep) if val.strip() != ""]


def centered_padding(val: str, amount: int, *, padding: str = " "):
    amount -= len(val)  # add __len__ to player class

    side_amount, extra = divmod(amount, 2)

    return (padding * (side_amount + extra)) + str(val) + (padding * side_amount)

class Cell:
    to_int_chars = 2

    def __init__(self, indexs: list[int], board_dimentions: list[int], *, human_readable_offset=1) -> None:
        self.indexs = indexs
        self.board_dimentions = board_dimentions

        self.human_readable_offset = human_readable_offset
        self.human_readable_loc = self._create_human_readable_loc()

        self.val = None

    # def __repr__(self) -> str:
        # return f"<'{__name__}.{self.__class__.__name__}' val={self.val} loc={self.loc}, human_readable_loc={self.human_readable_loc}>"

    def _create_human_readable_loc(self) -> str:
        if len(self.indexs) == 0:
            return ""


        to_int_amount = min(self.to_int_chars, len(self.indexs))

        letters = "".join([ALPHABET[index] for index in self.indexs[:-to_int_amount]])

        num = 0
        for i in range(to_int_amount, 0, -1):
            lower = i-1
            multiplyer = 1 if lower == 0 else self.board_dimentions[-lower]
            num += self.indexs[-i] * multiplyer

        return letters + str(num + self.human_readable_offset)

    def __repr__(self) -> str:
        return f"<'{__name__}.{self.__class__.__name__}' val={self.val}, indexs={self.indexs}, human_readable_loc={self.human_readable_loc}>" 

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.human_readable_loc if self.val is None else str(self.val)

class Board:
    def __init__(self, dimentions: list[int]) -> None:
        if any([item == 0 for item in dimentions]):
            dimentions = []
        self.dimentions = dimentions
        self.board = create_n_dimentional_list(self.dimentions, lambda indexs: Cell(indexs, self.dimentions))

        self.step_amount = 2

        self.offset = 1
        self.cell_size = len(str((self.dimentions[0] if len(self.dimentions) > 0 else 0) * (self.dimentions[1] if len(self.dimentions) > 1 else 1))) + (len(self.dimentions)-2 if len(self.dimentions) > 2 else 0)

        # signle line - ASKII
        self.verticle_line_char, self.horizontal_line_char, self.cross_line_char = "│", "─", "┼"

        # double line - ASKII
        # self.verticle_line_char, self.horizontal_line_char, self.cross_line_char = "║", "╬", "═"

        # simple - UTF-8
        # self.verticle_line_char, self.horizontal_line_char, self.cross_line_char = "|", "+", "-"

    def get(self, indexes: list[int]) -> str:
        if len(indexes) != len(self.dimentions):
            raise ValueError(
                f"Can not get location {str(indexes)[1:-1]} on {len(self.dimentions)}D board.")

        val = self.board
        for index in indexes:
            val = val[index]

        return val

    def set(self, indexes: list[int], value: str) -> None:
        if len(indexes) != len(self.dimentions):
            raise ValueError(
                f"Can not set value {repr(value)} location {str(indexes)[1:-1]} on {len(self.dimentions)}D board."
            )
        val = self.board
        for index in indexes[:-1]:
            val = val[index]
        val[indexes[-1]] = value

    def __repr__(self) -> str:
        return f"<'{__name__}.{self.__class__.__name__}' board={self.board}, dimentions={self.dimentions}>"

    def __str__(self) -> str:
        return repr(self)

board = Board([2, 2, 2, 2])
print(board.board)
print()
print(board)
