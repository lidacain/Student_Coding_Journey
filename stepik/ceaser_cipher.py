def decoder(lan, step, t):
    decode_text = ''
    if lan == 'ru':
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    else:
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in t:
        ch = False
        if letter.isupper():
            ch = True
            letter = letter.lower()
        if letter not in alphabet:
            decode_text += letter
        else:
            i = alphabet.find(letter)
            step_letter = step
            if i - step_letter <= -1 * len(alphabet) - 1:
                step_letter = (i - step_letter) % (-1 * len(alphabet) - 1)
            else:
                step_letter = i - step_letter
            if ch:
                decode_text += alphabet[step_letter].upper()
            else:
                decode_text += alphabet[step_letter]
    return decode_text

def encoder(lan, step, t):
    encode_text = ''
    if lan == 'ru':
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    else:
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in t:
        ch = False
        if letter.isupper():
            ch = True
            letter = letter.lower()
        if letter not in alphabet:
            encode_text += letter
        else:
            i = alphabet.find(letter)
            step_letter = step
            if step_letter + i >= len(alphabet):
                step_letter = (step_letter + i) % len(alphabet)
            else:
                step_letter = step_letter + i
            if ch:
                encode_text += alphabet[step_letter].upper()
            else:
                encode_text += alphabet[step_letter]
    return encode_text


print("Привет я могу шифровать или дешифровать шифр Цезаря.")
direction = input("Введите 'encode' если хотите зашифровать или 'decode' если хотите дешифровать текст - ")
language = input("Введите 'ru' если текст на русском языке или 'en' если текст на английском языке - ")
shift_step = int(input("Введите шаг сдвига (сдвиг вправо) - "))
text = input("Введите текст:\n")

if direction == 'encode':
    result = encoder(language, shift_step, text)
elif direction == 'decode':
    result = decoder(language, shift_step, text)
else:
    print("Неверное направление (encode/decode)")
    result = ""
print(result)

# for i in range(0, 26):
#     result = decoder(language, i, text)
#     print(i, result)
