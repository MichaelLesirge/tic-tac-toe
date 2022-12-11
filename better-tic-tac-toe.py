from typing import Optional, Any


def create_n_dimentional_list(dimentions: list[int]) -> Optional[list]:
    if len(dimentions) == 0:
        return None
    return [
        create_n_dimentional_list(dimentions[:-1]) for i in range(dimentions[-1])
    ]

def flatten(array: list) -> list:
    flat = []

    def flatten_secion(v):
        if isinstance(v, list):
            for item in v:
                flatten_secion(item)
        else:
            flat.append(v)
        
    flatten_secion(array)

    return flat

def split_ints(s: str, seps=(",", "x")):
    final_sep = seps[-1]
    for sep in seps[:-1]:
        s = s.replace(sep, final_sep)

    return [int(val.strip()) for val in s.split(final_sep) if val.strip() != ""]


class Board:
    def __init__(self, dimentions: list[int]) -> None:
        self.board = create_n_dimentional_list(dimentions)
        self.dimentions = dimentions

        self.str_template = self._create_template(self.board)

    def get(self, indexes: list[int]) -> Optional[str]:
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

    def __repr__(self) -> str:
        return f"<'{__name__}.{self.__class__.__name__}' board={self.board}, dimentions={str(self.dimentions)}>"

    def _create_template(self) -> str:
        final = ""
        def create_template(board, newline):
            pass


        create_template(self.board, False)
        return final

    def __str__(self) -> str:
        return self.str_template % flatten(self.board)

board = Board([3, 3])
print(flatten(board.board))