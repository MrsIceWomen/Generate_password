import secrets
import string
import unittest


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
    length = int(input('Введите длину пароля: '))
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


class TestPasswordFunc(unittest.TestCase):
    def test_generate_password(self):
        self.assertEqual(len(generate_password(10, True, True, True)), 10)
        self.assertEqual(len(generate_password(8, True, False, True)), 8)
        self.assertEqual(len(generate_password(12, False, True, False)), 12)
        with self.assertRaises(ValueError):
            generate_password(9, False, False, False)

    def test_assess_password_strength(self):
        self.assertEqual(assess_password_strength('zsdf123A@!pokj'), 4)
        self.assertEqual(assess_password_strength('zsdf123'), 3)
        self.assertEqual(assess_password_strength('123456'), 2)
        self.assertEqual(assess_password_strength('12'), 1)

    def test_mask_password(self):
        self.assertEqual(mask_password('1234567axd'), '**********')

    def test_get_user_preferences(self):
        length, use_letters, use_digits, use_specials = get_user_preferences()
        self.assertIsInstance(length, int)
        self.assertIsInstance(use_digits, bool)
        self.assertIsInstance(use_letters, bool)
        self.assertIsInstance(use_specials, bool)

    def test_save_password_to_file(self):
        test_filename = 'test_passwords.txt'
        test_password = 'test_password'
        save_password_to_file(test_password, test_filename)
        with open(test_filename, 'r') as file:
            lines = file.readlines()
            self.assertIn(test_password + '\n', lines)

    if __name__ == '__main__':
        unittest.main()
