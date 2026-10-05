from classes import Color, King, Queen, Bishop, Knight, Rook, Pawn


class Game:
    def __init__(self):
        self.board = [
            [
                Rook(Color.WHITE),
                Knight(Color.WHITE),
                Bishop(Color.WHITE),
                Queen(Color.WHITE),
                King(Color.WHITE),
                Bishop(Color.WHITE),
                Knight(Color.WHITE),
                Rook(Color.WHITE)
            ],
            [Pawn(Color.WHITE) for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn(Color.BLACK) for _ in range(8)],
            [
                Rook(Color.BLACK),
                Knight(Color.BLACK),
                Bishop(Color.BLACK),
                Queen(Color.BLACK),
                King(Color.BLACK),
                Bishop(Color.BLACK),
                Knight(Color.BLACK),
                Rook(Color.BLACK)
            ]
        ]
        self.turn = Color.WHITE

    def validate_move(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):
        if (
                ver_1 not in range(0, 8)
                or ver_2 not in range(0, 8)
                or hor_1 not in range(0, 8)
                or hor_2 not in range(0, 8)
                or (ver_1 == ver_2 and hor_1 == hor_2)
                or self.board[hor_1][ver_1] is None
        ):
            return False

        if (
                self.board[hor_2][ver_2] is not None
                and self.board[hor_1][ver_1].color == self.board[hor_2][ver_2].color
        ):
            return False


        figure = self.board[hor_1][ver_1]

        if figure.color != self.turn:
            return False

        return figure.can_move(ver_1, hor_1, ver_2, hor_2, self.board)

    def move(self, ver_1, hor_1, ver_2, hor_2):
        if not self.validate_move(ver_1, hor_1, ver_2, hor_2):
            return False

        self.board[hor_2][ver_2] = self.board[hor_1][ver_1]
        self.board[hor_1][ver_1] = None
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE

        self.board[hor_2][ver_2].marked_as_moved()

        return True
