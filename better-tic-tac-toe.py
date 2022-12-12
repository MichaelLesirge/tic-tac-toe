from math import ceil

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_INDEXS = {item: index for index, item in enumerate(ALPHABET)}


def create_n_dimentional_list(dimentions: list[int]) -> list:
    if len(dimentions) == 0:
        return None
    return [
        create_n_dimentional_list(dimentions[:-1]) for i in range(dimentions[-1])
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


class Board:
    def __init__(self, dimentions: list[int]) -> None:
        if any([item == 0 for item in dimentions]):
            dimentions = []
        self.dimentions = dimentions
        self.board = create_n_dimentional_list(self.dimentions)

        self.step_amount = 2

        self.offset = 1
        self.cell_size = len(str((self.dimentions[0] if len(self.dimentions) > 0 else 0) * (self.dimentions[1] if len(self.dimentions) > 1 else 1))) + (len(self.dimentions)-2 if len(self.dimentions) > 2 else 0)

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
                f"Can not set value {repr(value)} location {str(indexes)[1:-1]} on {len(self.dimentions)}D board.")
        val = self.board
        indexes = list(reversed(indexes))
        for index in indexes[:-1]:
            val = val[index]
        val[indexes[-1]] = value

    def __repr__(self) -> str:
        return f"<'{__name__}.{self.__class__.__name__}' board={self.board}, dimentions={str(self.dimentions)}>"

    def _create_template(self) -> str:
        # luckly this only happens once so it does not need to be super efficent
        def create_template(v, make_horizontal) -> str | list:
            """
            verticle, horizontal, verticle, horizontal...
            """
            if not isinstance(v, list):
                return "%s"

            v = [create_template(item, not make_horizontal) for item in v]

            if make_horizontal:
                rows = [item.split("\n") for item in v]
                sep = " " + self.verticle_line_char + " "

                if len(rows[0]) == 1:
                    return " " + (sep).join(v) + " "

                final = ""

                for i in range(len(rows) // 2):
                    for j in range(len(rows[i])):
                        final += rows[i][j] + sep + rows[i+1][j] + "\n"

                return final

            else:
                cells_count = v[0].count("%s")
                sep = self.horizontal_line_char * (self.cell_size + 2)

                return ("\n" + (self.cross_line_char.join([sep] * cells_count)) + "\n").join(v)

        return create_template(self.board, len(self.dimentions) % 2 == 1)

    def __str__(self) -> str:
        vals = []

        def make_vals(v: list | str, add=""):
            if not isinstance(v, list):
                if v is None:
                    if len(add) == 0:
                        v = ""
                    elif len(add) == 1:
                        v = str(ALPHABET_INDEXS[add] + self.offset)
                    else:
                        num = ((ALPHABET_INDEXS[add[-2]])*self.dimentions[0]) + ALPHABET_INDEXS[add[-1]]

                        v = str(num + self.offset)
                        if len(add)-2 > 0:
                            v = add[:-2] + v

                vals.append(centered_padding(str(v), self.cell_size))
            else:
                for index, item in enumerate(v):
                    make_vals(item, add + (ALPHABET[index]))

        make_vals(self.board)

        return self.str_template % tuple(vals)


board = Board([3, 3, 2])
print(board)
