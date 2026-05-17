import turtle

window = turtle.Screen()
window.setup(600, 600)
window.tracer(0)

class Figure:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        self.draw("black")
        window.update()

    def hide(self):
        self.draw("white")
        window.update()

    def draw(self, color):
        pass


class BoardGrid(Figure):
    def draw(self, color):
        self.t.clear()
        self.t.pencolor(color)
        self.t.pensize(5)
        self.t.penup()
        self.t.goto(-100, 300)
        self.t.pendown()
        self.t.goto(-100, -300)
        self.t.penup()
        self.t.goto(100, 300)
        self.t.pendown()
        self.t.goto(100, -300)
        self.t.penup()
        self.t.goto(-300, 100)
        self.t.pendown()
        self.t.goto(300, 100)
        self.t.penup()
        self.t.goto(-300, -100)
        self.t.pendown()
        self.t.goto(300, -100)

class Cross(Figure):
    def draw(self, color):
        self.t.clear()
        self.t.pencolor(color)
        self.t.pensize(6)
        self.t.penup()
        self.t.goto(self.x - 50, self.y + 50)
        self.t.pendown()
        self.t.goto(self.x + 50, self.y - 50)
        self.t.penup()
        self.t.goto(self.x - 50, self.y - 50)
        self.t.pendown()
        self.t.goto(self.x + 50, self.y + 50)


# Клас для Нулика
class Zero(Figure):
    def draw(self, color):
        self.t.clear()
        self.t.pencolor(color)
        self.t.pensize(6)
        self.t.penup()
        self.t.goto(self.x, self.y - 50)
        self.t.pendown()
        self.t.circle(50)


grid = BoardGrid()
grid.show()

matrix = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

turn = 1
game_active = True
figures_list = []


def check_win():
    for r in range(3):
        if matrix[r][0] == matrix[r][1] == matrix[r][2] != 0:
            return matrix[r][0]

    for c in range(3):
        if matrix[0][c] == matrix[1][c] == matrix[2][c] != 0:
            return matrix[0][c]

    # Діагоналі
    if matrix[0][0] == matrix[1][1] == matrix[2][2] != 0:
        return matrix[0][0]
    if matrix[0][2] == matrix[1][1] == matrix[2][0] != 0:
        return matrix[0][2]

    return 0


def click(x, y):
    global turn, game_active

    if not game_active:
        return

    if x < -100:
        col = 0
    elif x < 100:
        col = 1
    else:
        col = 2

    if y > 100:
        row = 0
    elif y > -100:
        row = 1
    else:
        row = 2

    if matrix[row][col] != 0:
        return

    matrix[row][col] = turn

    cx = 0
    cy = 0

    if col == 0:
        cx = -200
    elif col == 1:
        cx = 0
    elif col == 2:
        cx = 200

    if row == 0:
        cy = 200
    elif row == 1:
        cy = 0
    elif row == 2:
        cy = -200

    if turn == 1:
        f = Cross()
        f.setPosition(cx, cy)
        f.show()
        figures_list.append(f)
        turn = 2
    else:
        f = Zero()
        f.setPosition(cx, cy)
        f.show()
        figures_list.append(f)
        turn = 1

    winner = check_win()
    if winner != 0:
        print("Переможець: гравець", winner)
        game_active = False

    has_empty = False
    for r in range(3):
        for c in range(3):
            if matrix[r][c] == 0:
                has_empty = True

    if not has_empty and game_active:
        print("Нічия!")
        game_active = False


window.onclick(click)
window.listen()

window.mainloop()
