import geometry

lst = input('введите стандарную нотацию вида "B a1 - h8": ').split()
if len(lst) < 4:
    print("Некорректно расставлены пробелы. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif len(lst) > 4:
    print("Введены лишние данные. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif lst[0] not in frozenset("BRQPKN"):
    print("Некорректное обозначение фигуры. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif geometry.invalid_input_square(lst[1]):
    print("Неверно указано стартовое поле. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif lst[2] != "-":
    print(f"Введен некорректный разделитель {lst[2]} вместо '-'. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
elif geometry.invalid_input_square(lst[3]):
    print("Неверно указано конечное поле. Пожалуйста, введите стандартную нотацию вида 'B a1 - h8'")
else:
    figure = lst[0]

    block_1 = lst[1]
    block_2 = lst[3]

    hor_1 = int(block_1[1])
    ver_1 = block_1[0]

    hor_2 = int(block_2[1])
    ver_2 = block_2[0]

    output = geometry.validate_move(figure, ver_1, hor_1, ver_2, hor_2)
    
    print(output)


#Создаю доску и заполняю фигурами

keys_of_squares = []

for vertical in geometry.verticals:
    for horizontal in range(1, 9):
        res = vertical + str(horizontal)
        keys_of_squares.append(res)

board = dict.fromkeys(keys_of_squares)

ver_to_w_pounds = [ver + "2" for ver in geometry.verticals.keys()]
ver_to_b_pounds = [ver + "7" for ver in geometry.verticals.keys()]

for square in ver_to_w_pounds:
    board[square] = ("P", "w")

for square in ver_to_b_pounds:
    board[square] = ("P", "b")

ver_to_w_figures = [ver + "1" for ver in geometry.verticals.keys()]
ver_to_b_figures = [ver + "8" for ver in geometry.verticals.keys()]

figures = "RNBQKBNR"
i = 0
while i <= 7:
    board[ver_to_w_figures[i]] = (figures[i], "w")
    board[ver_to_b_figures[i]] = (figures[i], "b")
    i += 1