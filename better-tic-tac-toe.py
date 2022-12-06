class Board:
    def __init__(self, width=3, height=3, depth=1) -> None:
        self.board = [
            [
                [
                    None for k in range(width)
                ] for j in range(height)
            ] for i in range(depth)
        ]
        print(self.board)

Board(3, 3, 3)