from random import randint
import time


# Класс точек на доске

class Point:
    def __init__(self, x, y): # Координаты точки
        self.x = x
        self.y = y

    def __eq__(self, other): # сравнение координат
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # возвращение данных по точкам, проверка точек попадания по кораблю в списке точек корабля
        return f"Point({self.x}, {self.y}"

# Классы - исключения

class BoardException(Exception): # Общий класс исколючений
    pass

class BoardOutException(Exception): # Исключение выстрел мимо доски
    def __srt__(self):
        return "Выстрел за границу доски!"

class BoardUsedException(BoardException): # Исключение вовторный выстрел по клетке
    def __str__(self):
        return "Повторный выстрел в ту же клетку"

class BoardWrongShipException(BoardException): # Исключение для размещения кораблей
    pass


# Класс корабля на доске

# x, y — координаты начала корабля. bow - размер.
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l  # Длина корабля
        self.o = o  # положение корабля
        self.lives = l 

    @property # метод вычисления свойства точек
    def points(self):
        ship_points = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_points.append(Point(cur_x, cur_y))  # описание корабля списком точек

        return ship_points

    def shooten(self, shot):  # попали в корабль или нет
        return shot in self.points


# Класс игрового поля

class Board:
    def __init__(self, hid = False, size = 6):  # создание поля
        self.size = size
        self.hid = hid

        self.count = 0  # количество пораженных кораблей (переменная)

        self.field = [["O"] * size for _ in range(size)]  # сетка с определенным размером, в "0" клетка не занята, в нее не делали выстрел

        self.busy = []  # занятые точки (корабли, или точка выстрелов)
        self.ships = []  # список кораблей

    def __str__(self):  # вывод корабля на доску
        res = ""  # переменная, которая записывает игровое поле
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):  # в цикле проходим по строкам доски и по индекс строки через enumerate
            res += f"\n{i + 1} | " + " | ".join(row) + " |"  # выводим номер строки и через палочку клетки строки

        if self.hid:  # отвечает нужно ли скрывать корабли на доске, если истина, то пустые заменяет на квадратик
            res = res.replace("■", "O")
        return res

    def out(self, d):  # проверяет находится ли точка за пределами доски
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Очертания корабля и добавление его на поле боя

    def contour(self, ship, verb = False):
        near = [  # в списке объявление границ точек корабля для соблюдения условия, (0, 0) сама точка
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.points:
            for dx, dy in near: # в цикле по списку сдвигаем на dx, dy и проходим по всему полю
                cur = Point(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship): # метод для размещения кораблей, который проверит что не выходит за границы поля и не занята
        for d in ship.points:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException() #  выбрасываем исключение если ложь
        for d in ship.points:
            self.field[d.x][d.y] = "■"
            self.busy.append(d) # список занятых точек

        self.ships.append(ship) # список собственных кораблей
        self.contour(ship) # обводим по контуру корабль

# Стрельба

    def shot(self, d): # выстрел по полю
        if self.out(d):
            raise BoardOutException() # проверка попадаем в поле или нет

        if d in self.busy:
            raise BoardUsedException() # проверка занята точка или нет

        self.busy.append(d) # добавляем точка, что занята

        for ship in self.ships: # в цикле проходимся по полю
            if d in ship.points:
                ship.lives -= 1 # уменьшаем количество жизней корабля
                self.field[d.x][d.y] = "X" # пометка попаданияв корабля
                if ship.lives == 0: # если кончились у корабля жизни обводим по контуру точками
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!") # зцикливаемсообщением об уничтожении корабля
                    return False
                else:
                    print("Корабль ранен!") # корабль ранен и необходимо повторить ход
                    return True

        self.field[d.x][d.y] = "." # если промах то ставиться точка, с сообщением промах
        print("Промах!")
        return False


    def begin(self):
        self.busy = [] # список обнуляется до начала игры, до начала игры хранились точки

# Классы игроков

class Player:
    def __init__(self, board, opponent): # в качестве аргумента 2 доски
        self.board = board
        self.opponent = opponent

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True: # в цикле просим сделать бесконечный выстрел
            try:
                target = self.ask()
                repeat = self.opponent.shot(target)
                return repeat
            except BoardException as e:
                print(e)


# Класс противников

class AI(Player):
    def ask(self): # спрашиваем точки от 0 до 5 (запрос координат)
        d = Point(randint(0,5), randint(0, 5)) # случчайно генерируем от 0 до 5 точки
        print(f"Ход ИИ: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self): # запрос координат у игроков
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y) #  проверка что это числа
            return Point(x - 1, y - 1) # корректировка координат по индексу минус 1


# Основной класс игры

class Game:
    pass
    def try_board(self): # генерирование досок, заполненные кораблями (создание доски)
        lens = [3, 2, 2, 1, 1, 1, 1] #  определение количества и класса кораблей (расстановка кораблей)
        board = Board(size = self.size)
        attemps = 0
        for l in lens: # для каждой длины корабля в бесконечном цикле будет пытаться поставить на поле игровое
            while True:
                attemps += 1
                if attemps > 2000: # если итераций расстановки кораблей больше 2000 то возвращает пустую доску
                    return None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try: # добавление корабля
                    board.add_ship(ship)
                    break # если всё хорошо то останавливаем цикл
                except BoardWrongShipException:
                    pass # если исключение выдает, то итерация продолжается
        board.begin()
        return board

    def random_board(self): # метод случайного вызова игрового поля в бесконечном цикле
        board = None
        while board is None:
            board = self.try_board()
        return board

    def start(self):
        pass

# генератор конструктора случайного поля

    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

# Приветствие о начале игры

    def greet(self):
        print("--------------------------------------------------------")
        print("                Добро пожаловать в игру                 ")
        print("--------------------------------------------------------")
        print("---------------------Морской бой------------------------")
        print("--------------------------------------------------------")
        print("                  Режимы работы игры:                   ")
        print("--------------------------------------------------------")
        print(" Формат ввода : x y , где x это строка , а y это столбец ")
        print("--------------------------------------------------------")

    def game_loop(self): # игровой бесконечный цикл
        num = 0 # номер хода
        while True: # цикл вывода досок игроков
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска ИИ:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0: # определения номера хода, если номер четный то ходит пользователь, если не четный то ИИ
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит ИИ!")
                repeat = self.ai.move()
            if repeat: # записывание хода
                num -= 1 # уменьшаем количество хода, чтобы ход остался у тоже же игрока

            if self.ai.board.count == 7: # проверка количества пораженных кораблей которые остались на доске
                print("-" * 20)
                print("Пользователь выиграл!")
                time.sleep(10)
                break


            if self.us.board.count == 7:
                print("-" * 20)
                print("ИИ выиграл!")
                time.sleep(10)
                break

            num += 1


# Старт игры

    def start(self): # метод старт
        self.greet()
        self.game_loop()

g = Game()
g.start() # запуск игры