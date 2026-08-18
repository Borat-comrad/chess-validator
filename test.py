
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


lst = input('введите стандарную нотацию вида "B a1 - h8": ').split()

if len(lst) < 4:
    print("Некорректно расставлены пробелы. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif len(lst) > 4:
    print("Введены лишние данные. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif lst[0] not in frozenset("BRQPKN"):
    print("Некорректное обозначение фигуры. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif invalid_input_square(lst[1]):
    print("Неверно указано стартовое поле. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif lst[2] != "-":
    print(f"Введен некорректный разделитель {lst[2]} вместо '-'. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif invalid_input_square(lst[3]):
    print("Неверно указано конечное поле. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
else:
    figure = lst[0]

    block_1 = lst[1]
    block_2 = lst[3]

    hor_1 = int(block_1[1])
    ver_1 = block_1[0]

    hor_2 = int(block_2[1])
    ver_2 = block_2[0]

    output = validate_move(figure, ver_1, hor_1, ver_2, hor_2)
    
    print(output)


#Создаю доску и заполняю фигурами

keys_of_squares = []

for vertical in verticals:
    for horizontal in range(1, 9):
        res = vertical + str(horizontal)
        keys_of_squares.append(res)

board = dict.fromkeys(keys_of_squares)

ver_to_w_pounds = [ver + "2" for ver in verticals.keys()]
ver_to_b_pounds = [ver + "7" for ver in verticals.keys()]

for square in ver_to_w_pounds:
    board[square] = ("P", "w")

for square in ver_to_b_pounds:
    board[square] = ("P", "b")

ver_to_w_figures = [ver + "1" for ver in verticals.keys()]
ver_to_b_figures = [ver + "8" for ver in verticals.keys()]

figures = "RNBQKBNR"
i = 0
while i <= 7:
    board[ver_to_w_figures[i]] = (figures[i], "w")
    board[ver_to_b_figures[i]] = (figures[i], "b")
    i += 1