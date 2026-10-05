"""Тесты текущих правил. Шах, рокировка, превращение и en passant не проверяются.

Запуск: python -B tests_oop.py
Путь к проекту можно передать: python -B tests_oop.py D:/путь/к/проекту
Файл можно также положить рядом с Game.py и classes.py.
"""
import sys
from pathlib import Path

project = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
if not (project / "Game.py").exists() and len(sys.argv) == 1:
    project = Path("D:/misha/Desktop/kolya")
sys.dont_write_bytecode = True
sys.path.insert(0, str(project))

from Game import Game
from classes import Color, King, Queen, Bishop, Knight, Rook, Pawn

W, B = Color.WHITE, Color.BLACK


def coordinates(square):
    # Шахматные обозначения нужны только для читаемости тестовых данных.
    return ord(square[0]) - ord("a"), int(square[1]) - 1


def make_game(position, turn):
    game = Game()
    if position is not None:
        game.board = [[None for _ in range(8)] for _ in range(8)]
        for figure_class, color, square, in_start_pos in position:
            ver, hor = coordinates(square)
            game.board[hor][ver] = figure_class(color, in_start_pos)
    game.turn = turn
    return game


def snapshot(game):
    # Сохраняем ссылки и значения флагов, чтобы заметить изменения при проверке.
    return game.turn, tuple(
        tuple((figure, figure.color, figure.in_start_pos) if figure is not None else None
              for figure in row)
        for row in game.board
    )


# Формат: описание, позиция, очередь, исходная клетка, конечная, ожидаемый ответ.
# Позиция None означает начальную расстановку.
# Каждая фигура задаётся как (класс, цвет, клетка, начальный статус).
# Каждый тест получает НОВУЮ игру и НОВЫЕ объекты фигур.
tests = [
    ("Начало: e2-e4", None, W, "e2", "e4", True),
    ("Начало: конь перепрыгивает пешки", None, W, "b1", "c3", True),
    ("Начало: ладье мешает пешка", None, W, "a1", "a4", False),
    ("Начало: слону мешает пешка", None, W, "c1", "f4", False),
    ("Начало: ферзю мешает пешка", None, W, "d1", "d4", False),
    ("Конечная клетка занята своей", None, W, "b1", "d2", False),
    ("Чёрные не ходят первыми", None, W, "e7", "e5", False),
    ("Пустая исходная клетка", None, W, "e3", "e4", False),
    ("Ход на месте", None, W, "e2", "e2", False),
    ("Исходная вертикаль ниже нуля", None, W, "`2", "a3", False),
    ("Исходная вертикаль выше семи", None, W, "i2", "a3", False),
    ("Исходная горизонталь ниже нуля", None, W, "a0", "a3", False),
    ("Исходная горизонталь выше семи", None, W, "a9", "a3", False),
    ("Конечная вертикаль ниже нуля", None, W, "a2", "`3", False),
    ("Конечная вертикаль выше семи", None, W, "a2", "i3", False),
    ("Конечная горизонталь ниже нуля", None, W, "a2", "a0", False),
    ("Конечная горизонталь выше семи", None, W, "a2", "a9", False),
]

# Свободные пути в обоих направлениях, включая все четыре диагонали.
for kind, routes in (
    (Rook, (("a4", "h4"), ("h4", "a4"), ("d1", "d8"), ("d8", "d1"))),
    (Bishop, (("a1", "h8"), ("h8", "a1"), ("a8", "h1"), ("h1", "a8"))),
    (Queen, (("a4", "h4"), ("h4", "a4"), ("d1", "d8"), ("d8", "d1"),
             ("a1", "h8"), ("h8", "a1"), ("a8", "h1"), ("h1", "a8"))),
):
    for start, end in routes:
        tests.append((f"{kind.__name__}: свободный путь {start}-{end}",
                      ((kind, W, start, False),), W, start, end, True))

# Препятствия, взятие на конечной клетке и неправильная геометрия.
for kind, start, end, middle, wrong in (
    (Rook, "a4", "h4", "d4", "b5"),
    (Bishop, "a1", "h8", "d4", "a4"),
    (Queen, "h8", "a1", "d4", "f7"),
):
    origin = ((kind, W, start, False),)
    for color in (W, B):
        tests.append((f"{kind.__name__}: препятствие {color.name}",
                      origin + ((Pawn, color, middle, False),), W, start, end, False))
    tests.append((f"{kind.__name__}: взятие на конечной клетке",
                  origin + ((Knight, B, end, False),), W, start, end, True))
    tests.append((f"{kind.__name__}: своя на конечной клетке",
                  origin + ((Knight, W, end, False),), W, start, end, False))
    tests.append((f"{kind.__name__}: неправильная геометрия",
                  origin, W, start, wrong, False))

for kind, start, end, expected in (
    (King, "e4", "f4", True), (King, "e4", "e5", True),
    (King, "e4", "f5", True), (King, "e4", "e6", False),
    (Knight, "d4", "e6", True), (Knight, "d4", "f5", True),
    (Knight, "d4", "b3", True), (Knight, "d4", "e5", False),
):
    tests.append((f"{kind.__name__}: {start}-{end}",
                  ((kind, W, start, False),), W, start, end, expected))

# Пешки обоих цветов. Взятие на проходе сюда не входит.
for color, enemy, start, forward, double, backward, left, right in (
    (W, B, "e2", "e3", "e4", "e1", "d3", "f3"),
    (B, W, "e7", "e6", "e5", "e8", "d6", "f6"),
):
    origin = ((Pawn, color, start, True),)
    cases = [
        ("шаг вперёд", origin, forward, True),
        ("двойной шаг", origin, double, True),
        ("назад", origin, backward, False),
        ("вбок", origin, "d" + start[1], False),
        ("диагональ на пустую клетку", origin, left, False),
        ("диагональ на пустую клетку справа", origin, right, False),
        ("повторный двойной шаг", ((Pawn, color, start, False),), double, False),
        ("обычный шаг после первого хода", ((Pawn, color, start, False),), forward, True),
        ("своя мешает двойному шагу", origin + ((Knight, color, forward, False),), double, False),
        ("чужая мешает двойному шагу", origin + ((Knight, enemy, forward, False),), double, False),
        ("занят конец двойного шага", origin + ((Knight, enemy, double, False),), double, False),
        ("чужая прямо впереди", origin + ((Knight, enemy, forward, False),), forward, False),
        ("своя прямо впереди", origin + ((Knight, color, forward, False),), forward, False),
        ("взятие влево", origin + ((Knight, enemy, left, False),), left, True),
        ("взятие вправо", origin + ((Knight, enemy, right, False),), right, True),
        ("своя по диагонали", origin + ((Knight, color, left, False),), left, False),
        ("взятие назад", origin + ((Knight, enemy, "d" + backward[1], False),), "d" + backward[1], False),
    ]
    for title, position, end, expected in cases:
        tests.append((f"Пешка {color.name}: {title}", position, color, start, end, expected))

passed = 0
failed = 0


def report(title, ok, details=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"OK: {title}")
    else:
        failed += 1
        print(f"FAIL: {title}. {details}")


for title, position, turn, start, end, expected in tests:
    game = make_game(position, turn)
    args = (*coordinates(start), *coordinates(end))
    before = snapshot(game)
    try:
        actual = game.validate_move(*args)
        repeated = game.validate_move(*args)
        ok = actual is expected and repeated is expected and snapshot(game) == before
        report(title, ok, f"ожидалось {expected}, получено {actual}, повторно {repeated}; "
               f"состояние сохранено: {snapshot(game) == before}")
    except Exception as error:
        report(title, False, f"{type(error).__name__}: {error}")

# Последовательность настоящих ходов: очередь, флаги, ссылки и неизменность отказа.
game = Game()
moves = (
    ("e7", "e5", False),
    ("e2", "e4", True),
    ("d2", "d4", False),
    ("d7", "d5", True),
    ("e4", "e6", False),
    ("e4", "d5", True),
)
for start, end, expected in moves:
    v1, h1 = coordinates(start)
    v2, h2 = coordinates(end)
    figure = game.board[h1][v1]
    before = snapshot(game)
    old_turn = game.turn
    try:
        actual = game.move(v1, h1, v2, h2)
        if expected:
            other_cells_unchanged = all(
                (game.board[h][v], game.board[h][v].color, game.board[h][v].in_start_pos)
                == before[1][h][v] if game.board[h][v] is not None else before[1][h][v] is None
                for h in range(8) for v in range(8)
                if (v, h) not in ((v1, h1), (v2, h2))
            )
            ok = (actual is True and game.board[h1][v1] is None
                  and game.board[h2][v2] is figure and figure.in_start_pos is False
                  and game.turn == (B if old_turn == W else W) and other_cells_unchanged)
        else:
            ok = actual is False and snapshot(game) == before
        report(f"Выполнение {start}-{end}", ok, f"ожидалось {expected}, получено {actual}; проверяются и изменения состояния")
    except Exception as error:
        report(f"Выполнение {start}-{end}", False, f"{type(error).__name__}: {error}")

game_1, game_2 = Game(), Game()
before = snapshot(game_2)
try:
    moved = game_1.move(4, 1, 4, 3)
    report("Две партии независимы", moved is True and snapshot(game_2) == before
           and game_1.board[3][4] is not game_2.board[1][4])
except Exception as error:
    report("Две партии независимы", False, f"{type(error).__name__}: {error}")

print(f"\nВсего: {passed + failed}. Успешно: {passed}. Ошибок: {failed}.")
sys.exit(1 if failed else 0)
