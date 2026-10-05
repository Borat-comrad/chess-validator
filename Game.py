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


    # Реализация првоерки безопасности короля:

    def get_tmp_board(self):
        """
        Безопасность короля:
        Создает временную доску - копию текущей для моделирования проверки безопасности короля.
        Копирует вложенную стрктуру доски(список списков), но оставляет ссылки на те же обьекты фигур(подразумевается, что обьекты не меняются при проверке)
        """
        tmp_board = []
        for row in self.board:
            new_row = row[:]
            tmp_board.append(new_row)
        return tmp_board

    def emulate_move(self, ver_1, hor_1, ver_2, hor_2):
        """
        Безопасность короля:
        Дедает ход на времменной доске
        """

        tmp_board = self.get_tmp_board()
        tmp_board[hor_2][ver_2] = tmp_board[hor_1][ver_1]
        tmp_board[hor_1][ver_1] = None

        return tmp_board


    def get_kings_square(self, tmp_board):
        """
        Безопасность короля:
        Возвращает координаты короля
        """

        for hor, row in enumerate(tmp_board):
            for ver, figure in enumerate(row):
                if isinstance(figure, King) and figure.color == self.turn:
                    return ver, hor


    def king_safe_check(self, ver_1, hor_1, ver_2, hor_2):
        """
        Безопасность короля:
        Для каждой фигуры противника проверяем, атакует ли она клетку короля
        """

        tmp_board = self.emulate_move(ver_1, hor_1, ver_2, hor_2)

        kings_square = self.get_kings_square(tmp_board)

        for hor, row in enumerate(tmp_board):
            for ver, figure in enumerate(row):
                if figure is None:
                    continue
                if figure.color != self.turn:
                    if isinstance(figure, Pawn) and figure.capture_can_move(ver, hor, kings_square[0], kings_square[1]):
                        return False
                    elif (not isinstance(figure, Pawn)) and figure.can_move(ver, hor, kings_square[0], kings_square[1], tmp_board):
                        return False

        return True

