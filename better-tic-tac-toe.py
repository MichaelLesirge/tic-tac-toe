def create_board(*dimentions: int) -> list:
    if len(dimentions) == 0:
        return None
    return [
        create_board(*dimentions[:-1]) for i in range(dimentions[-1])
    ]


def split_ints(s: str, seps=(",", "x")):
    final_sep = seps[-1]
    for sep in seps[:-1]:
        s = s.replace(sep, final_sep)

    return [int(val.strip()) for val in s.split(final_sep) if val.strip() != ""]

class Board:
    def __init__(self, *dimentions: int) -> None:
        self.board = create_board(*dimentions)
        self.dimentions = dimentions

    def __repr__(self) -> str:
        return f"<'{__name__}.{self.__class__.__name__}' board={self.board}, dimentions={str(self.dimentions)}>"


print(split_ints("2,3,,,4"))
