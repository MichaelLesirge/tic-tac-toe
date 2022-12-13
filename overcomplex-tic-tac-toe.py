from math import ceil

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


print("THIS IS A WORK IN PROGRESS")
print("Try a different project for now")
print()

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
        # if len(dimentions) > 3:
        #     raise ValueError(f"Why one earth do you want to play {len(dimentions)}D tic-tac-toe?")

        self.dimentions = dimentions
        self.board = create_n_dimentional_list(self.dimentions, lambda indexs: Cell(indexs, self.dimentions))

        self.step_amount = 2

        buttom_cell = self.board
        while isinstance(buttom_cell, list):
            buttom_cell = buttom_cell[-1]

        self.cell_size = len(str(buttom_cell))

        # signle line - ASKII
        self.verticle_line_char, self.horizontal_line_char, self.cross_line_char = "│", "─", "┼"

        # double line - ASKII
        # self.verticle_line_char, self.horizontal_line_char, self.cross_line_char = "║", "╬", "═"

        # simple - UTF-8
        # self.verticle_line_char, self.horizontal_line_char, self.cross_line_char = "|", "+", "-"

        self.str_template = self._create_template()

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

    def _create_template(self) -> str:
        # luckly this only happens once so it does not need to be super efficent

        def create_template(v, make_horizontal) -> str | list:
            if not isinstance(v, list):
                return "%s"

            # Maybe try going up the chain not down it
            v = [create_template(item, not make_horizontal) for item in v]

            if make_horizontal:
                rows = [item.split("\n") for item in v]
                sep = " " + self.verticle_line_char + " "

                if len(rows[0]) == 1:
                    return " " + (sep).join(v) + " "

                final = ""

                for i in range(len(rows[0])):
                    final += sep.join([item[i] for item in rows])
                    final += "\n"

                return final

            else:
                if isinstance(v[0], str):
                    count = v[0].count("%s")
                else:
                    count = len(v[0]) + 1

                sep = self.horizontal_line_char * (self.cell_size + 2)

                return ("\n" + (self.cross_line_char.join([sep] * count)) + "\n").join(v)

        return create_template(self.board, len(self.dimentions) % 2 == 1)

    def __repr__(self) -> str:
        return f"<'{__name__}.{self.__class__.__name__}' board={self.board}, dimentions={self.dimentions}>"

    def __str__(self) -> str:
        print(self.board)
        return self.str_template.replace("%s", " " * self.cell_size)


size = [3, 3, 3]
board = Board(list(reversed(size)))
print(board)
