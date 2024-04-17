from random import choice


def generator(l_ans, d_ans, l_l_ans, u_l_ans, p_ans, e_ans):
    l_ans = int(l_ans)
    d_ans = d_ans.lower()
    l_l_ans = l_l_ans.lower()
    u_l_ans = u_l_ans.lower()
    p_ans = p_ans.lower()
    e_ans = e_ans.lower()
    password = ''
    digits_case = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lower_letter_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                         'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                         's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper_letter_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                         'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    punctuation_case = ['!', '#', '$', '%', '&', '*', '+', '-', '=', '?', '@', '^', '_']
    exception_case = ['i', 'l', '1', 'L', 'o', '0', 'O']
    r = ['d', 'l', 'u', 'p']
    while l_ans != 0:
        case = choice(r)
        if d_ans == 'д' and case == 'd':
            symbol = choice(digits_case)
            if e_ans == 'д' and symbol in exception_case:
                continue
            else:
                password += symbol
                l_ans -= 1
        if l_l_ans == 'д' and case == 'l':
            symbol = choice(lower_letter_case)
            if e_ans == 'д' and symbol in exception_case:
                continue
            else:
                password += symbol
                l_ans -= 1
        if u_l_ans == 'д' and case == 'u':
            symbol = choice(upper_letter_case)
            if e_ans == 'д' and symbol in exception_case:
                continue
            else:
                password += symbol
                l_ans -= 1
        if p_ans == 'д' and case == 'p':
            symbol = choice(punctuation_case)
            if e_ans == 'д' and symbol in exception_case:
                continue
            else:
                password += symbol
                l_ans -= 1
    return password


print("Здраствуйте я могу сгенерировать любой пароль по вашим требованиям.")
print("Выберите длину пароля и из каких символов он будет сосотоять:")
length = int(input("Введите длину пароля - "))
digits = input("Хотите чтобы в вашем пароле были цифры? (д - Да, н - Нет) - ").strip()
lower_letter = input("Хотите чтобы в вашем пароле были буквы нижнего регистра? (д - Да, н - Нет) - ").strip()
upper_letter = input("Хотите чтобы в вашем пароле были буквы верхнего регистра? (д - Да, н - Нет) - ").strip()
punctuation = input("Хотите чтобы в вашем пароле были специальный симолы? (д - Да, н - Нет) - ").strip()
exception = input("Хотите чтобы я исключил неоднозначные символы [il1Lo0O]? (д - Да, н - Нет) - ").strip()
print("Ваш пароль - ", generator(length, digits, lower_letter, upper_letter, punctuation, exception))

