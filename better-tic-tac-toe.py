def create_board(*dimentions):
    if len(dimentions) == 0:
        return None
    return [
       create_board(*dimentions[:-1]) for i in range(dimentions[-1])
    ]

class Board:
    def __init__(self, *dimentions) -> None:
        self.board = create_board(*dimentions)
        self.dimentions = dimentions

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{str(self.dimentions)}"
    


x = Board(4)
print(x)