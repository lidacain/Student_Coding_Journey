from random import *


def is_valid(arg, b):
    if arg > b or arg < 1:
        return False
    return True


def number_guessing_game(h_n, b):
    number_of_attempts = 0
    while True:
        number = int(input(f"Введи целое число от 1 до {b}:\n"))
        number_of_attempts += 1
        if not is_valid(number, b):
            print(f"А может быть все-таки введем целое число от 1 до {b}?")
            continue
        if number == h_n:
            print()
            print("Вы угадали, поздравляем!")
            print("Вы угадали число с", number_of_attempts, "попытки")
            print()
            break
        elif number < h_n:
            print('Ваше число МЕНЬШЕ загаданного, попробуйте еще разок')
            continue
        else:
            print('Ваше число БОЛЬШЕ загаданного, попробуйте еще разок')
            continue


print("Добро пожаловать в числовую угадайку")
border = int(input("Введите правую границу загаданного числа (от 1 до сколько будет загадано число):\n"))
hidden_number = randint(1, border)
number_guessing_game(hidden_number, border)

while True:
    print("Хотите продолжить играть? (Y - Да, N - Нет)")
    answer = input()
    if answer == 'Y':
        border = int(input("Введите правую границу загаданного числа (от 1 до сколько будет загадано число):\n"))
        hidden_number = randint(1, border)
        number_guessing_game(hidden_number, border)
    else:
        print()
        print("Спасибо, что играли в числовую угадайку. Еще увидимся...")
        break


