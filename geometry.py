verticals = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
}

def movement_ban(ver_1: str, hor_1: int, ver_2: str, hor_2: int):
    return (
            ver_1 not in verticals
            or ver_2 not in verticals
            or (hor_1 not in range(1, 9))
            or (hor_2 not in range(1, 9))
            or (ver_1 == ver_2 and hor_1 == hor_2)
    )


def bishop_can_move(ver_1: str, hor_1: int, ver_2: str, hor_2: int):
    if movement_ban(ver_1, hor_1, ver_2, hor_2):
        return False

    return abs(verticals[ver_1] - verticals[ver_2]) == abs(hor_1 - hor_2)


def rook_can_move(ver_1: str, hor_1: int, ver_2: str, hor_2: int):
    if movement_ban(ver_1, hor_1, ver_2, hor_2):
        return False

    return ver_1 == ver_2 or hor_1 == hor_2


def queen_can_move(ver_1: str, hor_1: int, ver_2: str, hor_2: int):
    return bishop_can_move(ver_1, hor_1, ver_2, hor_2) or rook_can_move(ver_1, hor_1, ver_2, hor_2)


def pawn_can_move(ver_1: str, hor_1: int, ver_2: str, hor_2: int, color = "w", is_take = False):
    start_pos = 2 if color == "w" else 7
    direction = 1 if color == "w" else -1
    if not is_take:
        if (
                movement_ban(ver_1, hor_1, ver_2, hor_2)
                or hor_1 == start_pos - direction
                or ver_1 != ver_2
        ):
            return False

        return(
            hor_2 - hor_1 == direction
            or ((hor_1 == start_pos) and (hor_2 - hor_1 == 2 * direction))
        )

    if (
            movement_ban(ver_1, hor_1, ver_2, hor_2)
            or hor_1 == start_pos - direction
    ):
        return False

    return (
            hor_2 - hor_1 == direction
            and abs(verticals[ver_1] - verticals[ver_2]) == 1
            )


def king_can_move(ver_1: str, hor_1: int, ver_2: str, hor_2: int):
    if movement_ban(ver_1, hor_1, ver_2, hor_2):
        return False

    return (
            abs(hor_1 - hor_2) in (0, 1)
            and abs(verticals[ver_1] - verticals[ver_2]) in (0, 1)
        )



def knight_can_move(ver_1: str, hor_1: int, ver_2: str, hor_2: int):
    if movement_ban(ver_1, hor_1, ver_2, hor_2):
            return False

    return (
        (abs(verticals[ver_1] - verticals[ver_2]) == 2 and abs(hor_1 - hor_2) == 1)
        or (abs(verticals[ver_1] - verticals[ver_2]) == 1 and abs(hor_1 - hor_2) == 2)
    )



def validate_move(figure: str, ver_1: str, hor_1: int, ver_2: str, hor_2: int, color: object = "w", is_take: object = False) -> bool:
    if figure == "B":
        res = bishop_can_move(ver_1, hor_1, ver_2, hor_2)
    elif figure == "R":
        res = rook_can_move(ver_1, hor_1, ver_2, hor_2)
    elif figure == "Q":
        res = queen_can_move(ver_1, hor_1, ver_2, hor_2)
    elif figure == "P":
        res = pawn_can_move(ver_1, hor_1, ver_2, hor_2, color, is_take)
    elif figure == "K":
        res = king_can_move(ver_1, hor_1, ver_2, hor_2)
    elif figure ==  "N":
        res = knight_can_move(ver_1, hor_1, ver_2, hor_2)
    else:
        res = False
    return res

def invalid_input_square(square: str):
    if len(square) != 2:
        return True

    try:
        hor = int(square[1])
    except ValueError:
        return True
    return square[0] not in frozenset("abcdefgh") or hor not in range(1, 9)