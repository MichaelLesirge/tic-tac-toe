def create_board(*dimentions):
    if len(dimentions) == 0:
        return None
    return [
       create_board(*dimentions[:-1]) for i in range(dimentions[-1])
    ]

class Board:
    def __init__(self, *dimentions) -> None:
        self.board = create_board(*dimentions)
        print(self.board)

Board(4, 3, 2)