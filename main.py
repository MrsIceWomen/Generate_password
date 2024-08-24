import secrets
import string


def generate_password(length, use_letters, use_digits, use_specials):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_specials:
        characters += string.punctuation
    if not characters:
        raise ValueError('Не выбраны символы для генерации пароля.')
    return ''.join(secrets.choice(characters) for _ in range(length))


def get_user_preferences():
    while True:
        length = int(input('Введите длину пароля: '))
        if length > 0:
            break
        else:
            print('Длина пароля должна быть положительным числом.')
    use_letters = input('Добавить буквы? (да/нет) ').lower() == 'да'
    use_digits = input('Добавить цифры? (да/нет) ').lower() == 'да'
    use_specials = input('Добавить спецсимволы? (да/нет) ').lower() == 'да'
    return length, use_letters, use_digits, use_specials


def save_password_to_file(password, filename='passwords.txt'):
    with open(filename, 'a') as file:
        file.write(password + '\n')


def assess_password_strength(password):
    length_score = min(1, len(password) // 4)
    char_variety_score = (any(c.islower() for c in password) +
                          any(c.isupper() for c in password) +
                          any(c.isdigit() for c in password) +
                          any(c in string.punctuation for c in password))
    total_score = min(4, length_score + char_variety_score)
    return total_score


def mask_password(password):
    return '*' * len(password)


def main():
    try:
        length, use_letters, use_digits, use_specials = get_user_preferences()
        password = generate_password(length, use_letters, use_digits, use_specials)

        mask_choice = input('Замаскировать пароль при выводе? (да/нет) ').lower() == 'да'
        if mask_choice:
            print(f'Ваш пароль: {mask_password(password)}')
        else:
            print(f'Ваш пароль: {password}')

        strength = assess_password_strength(password)
        print(f'Сложность: {strength} из 4.')

        save_password = input('Сохранить в файл? (да/нет) ').lower() == 'да'
        if save_password:
            save_password_to_file(password)
            print(f'Сохранен пароль {password}!')
    except ValueError as e:
        print(f'Ошибка: {e}')


if __name__ == '__main__':
    main()
    
