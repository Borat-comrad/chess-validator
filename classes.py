from enum import Enum


class Color(Enum):
    WHITE = "white"
    BLACK = "black"


class TypeOfCastling(Enum):
    SHORT = "short"
    LONG = "long"


class Figure:

    def __init__(self, color: Color, in_start_pos: bool = True):
        self.color = color
        self.in_start_pos = in_start_pos

    def marked_as_moved(self):
        self.in_start_pos = False

    def is_path_clear(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int, board):
        if hor_2 < hor_1:
            hor_step = -1
        elif hor_2 > hor_1:
            hor_step = 1
        else:
            hor_step = 0

        if ver_2 < ver_1:
            ver_step = -1
        elif ver_2 > ver_1:
            ver_step = 1
        else:
            ver_step = 0

        curr_hor = hor_1 + hor_step
        curr_ver = ver_1 + ver_step

        while (
                curr_ver != ver_2
                or curr_hor != hor_2
        ):
            if board[curr_hor][curr_ver] is not None:
                return False

            curr_hor += hor_step
            curr_ver += ver_step

        return True


class King(Figure):
    def geom_validate(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):
        return (
                abs(hor_1 - hor_2) in (0, 1)
                and abs(ver_1 - ver_2) in (0, 1)
        )

    def can_move(self, ver_1, hor_1, ver_2, hor_2, board):
        return self.geom_validate(ver_1, hor_1, ver_2, hor_2)

    def attacks_square(self, ver_1, hor_1, ver_2, hor_2, board):
        """Проверяет, атакует ли фигура заданную клетку"""

        return self.can_move(ver_1, hor_1, ver_2, hor_2, board)


class Queen(Figure):
    def geom_validate(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):
        return (abs(ver_1 - ver_2) == abs(hor_1 - hor_2)) or (ver_1 == ver_2 or hor_1 == hor_2)

    def can_move(self, ver_1, hor_1, ver_2, hor_2, board):
        return self.geom_validate(ver_1, hor_1, ver_2, hor_2) and self.is_path_clear(ver_1, hor_1, ver_2, hor_2, board)

    def attacks_square(self, ver_1, hor_1, ver_2, hor_2, board):
        """Проверяет, атакует ли фигура заданную клетку"""

        return self.can_move(ver_1, hor_1, ver_2, hor_2, board)


class Bishop(Figure):
    def geom_validate(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):
        return abs(ver_1 - ver_2) == abs(hor_1 - hor_2)

    def can_move(self, ver_1, hor_1, ver_2, hor_2, board):
        return self.geom_validate(ver_1, hor_1, ver_2, hor_2) and self.is_path_clear(ver_1, hor_1, ver_2, hor_2, board)

    def attacks_square(self, ver_1, hor_1, ver_2, hor_2, board):
        """Проверяет, атакует ли фигура заданную клетку"""

        return self.can_move(ver_1, hor_1, ver_2, hor_2, board)


class Knight(Figure):
    def geom_validate(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):
        return (
                (abs(ver_1 - ver_2) == 2 and abs(hor_1 - hor_2) == 1)
                or (abs(ver_1 - ver_2) == 1 and abs(hor_1 - hor_2) == 2)
        )

    def can_move(self, ver_1, hor_1, ver_2, hor_2, board):
        return self.geom_validate(ver_1, hor_1, ver_2, hor_2)

    def attacks_square(self, ver_1, hor_1, ver_2, hor_2, board):
        """Проверяет, атакует ли фигура заданную клетку"""

        return self.can_move(ver_1, hor_1, ver_2, hor_2, board)


class Rook(Figure):
    def geom_validate(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):
        return ver_1 == ver_2 or hor_1 == hor_2

    def can_move(self, ver_1, hor_1, ver_2, hor_2, board):
        return self.geom_validate(ver_1, hor_1, ver_2, hor_2) and self.is_path_clear(ver_1, hor_1, ver_2, hor_2, board)

    def attacks_square(self, ver_1, hor_1, ver_2, hor_2, board):
        """Проверяет, атакует ли фигура заданную клетку"""

        return self.can_move(ver_1, hor_1, ver_2, hor_2, board)


class Pawn(Figure):
    def geom_validate(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int):

        if ver_1 != ver_2:
            return False

        direction = 1 if self.color == Color.WHITE else -1

        result = (
                hor_2 - hor_1 == direction
                or (self.in_start_pos is True and hor_2 - hor_1 == 2 * direction)
        )

        return result

    def is_pawn_path_clear(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int, board):
        """Проверяет отсутвие препятствия для пешки при дойном ходе"""

        direction = 1 if self.color == Color.WHITE else -1

        if abs(hor_2 - hor_1) == 2:
            if board[hor_1 + direction][ver_2] is not None:
                return False
        return True

    def capture_can_move(self, ver_1, hor_1, ver_2, hor_2):
        """Отдельно проверяет корректность взятия пешкой по диагонали"""

        direction = 1 if self.color == Color.WHITE else -1

        if not (
                hor_2 - hor_1 == direction
                and abs(ver_2 - ver_1) == 1
        ):
            return False

        return True

    def can_move(self, ver_1: int, hor_1: int, ver_2: int, hor_2: int, board):
        if board[hor_2][ver_2] is not None:
            return self.capture_can_move(ver_1, hor_1, ver_2, hor_2)

        return self.geom_validate(ver_1, hor_1, ver_2, hor_2) and self.is_pawn_path_clear(
            ver_1, hor_1, ver_2, hor_2, board
        )

    def attacks_square(self, ver_1, hor_1, ver_2, hor_2, board):
        """Проверяет, атакует ли фигура заданную клетку"""

        return self.capture_can_move(ver_1, hor_1, ver_2, hor_2)
