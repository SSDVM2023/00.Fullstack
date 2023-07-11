
import time

def greet():
    print("                Приветствуем вас в приложении           ")
    print("--------------------------------------------------------")
    print("--------------------Крестики-нолики---------------------")
    print("--------------------------------------------------------")
    print("                     Режимы работы:                     ")
    print("--------------------------------------------------------")
    print(" Формат ввода : 1-2 , где 1 это строка , а 2 это столбец ")
    print("--------------------------------------------------------")

def print_board(board):
    print("  | 0 | 1 | 2 |")
    print("--------------")
    for row in range(3):
        print(f"{row} | {' | '.join(board[row])} |")
        print("--------------")

def input_rules():
    number = None
    while number is None:
        num_str = input("Введите номер строки и номер столбца: ")
        if len(num_str) == 3:
            if "-" in num_str:
                my_list = list(num_str.split('-'))
                if my_list[0].isdigit() and my_list[1].isdigit():
                    row = int(my_list[0])
                    col = int(my_list[1])
                    if 0 <= row <= 2 and 0 <= col <= 2:
                        number = num_str
                    else:
                        print("Введены некорректные значения строки и/или столбца")
                else:
                    print("Введены некорректные значения строки и/или столбца")
            else:
                print("Отсутствует '-'")
        else:
            print("Вы ввели некорректное значение")
    return list(number.split("-"))



def check_winner(board, player):
    
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True  
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    if board[2][0] == board[1][1] == board[0][2] == player:
        return True

    return False


def game():
    greet()  # Вывод приветствия
    board = [[' ' for _ in range(3)] for _ in range(3)]  # Создание пустого поля
    print(" Формат поля: ")
    print_board(board)  # Вывод поля на экран
    current_player = 'X'  # Игрок, который сейчас ходит
    while True:  # Бесконечный цикл игры
        coords = input_rules()  # Ввод номера строки и столбца
        row = int(coords[0])  # Получение значения строки
        col = int(coords[1])  # Получение значения столбца
        if board[row][col] == ' ':  # Проверка, что выбранная ячейка пуста
            board[row][col] = current_player  # Запись символа текущего игрока в выбранную ячейку
            print_board(board)  # Вывод обновленного поля на экран

            if check_winner(board, current_player):  # Проверка победы текущего игрока
                print(f"Игрок {current_player} победил!")
                time.sleep( 5 )
                break  # Выход из игры

            if all(board[row][col] != ' ' for row in range(3) for col in range(3)):
                print("Ничья!")
                time.sleep( 5 )
                break  # Выход из игры

            current_player = 'O' if current_player == 'X' else 'X'  # Смена игрока
        else:
            print("Данная ячейка уже занята!!!!!!!!!!")  # Вывод сообщения об ошибке, если ячейка уже занята


game()

