# *Генератор паролей*


Эта программа генерирует безопасные пароли на основе предпочтений пользователя, используя библиотеки Python secrets и string для криптографически безопасной генерации.

## Возможности

- Настраиваемая генерация паролей: Пользователь может выбрать длину и типы символов (буквы, цифры, спецсимволы).
- Оценка сложности пароля: Оценивает сложность пароля по шкале от 1 до 4.
- Маскирование пароля: Возможность отображения пароля в виде звездочек.
- Сохранение в файл: Сохранение сгенерированных паролей в файл.

## Объяснение кода

### Импорт

```python
import secrets
import string
```

- **`secrets`**: Обеспечивает функции для генерации криптографически безопасныхг случайных чисел.
- **`string`**: Содержит строковые константы, такие как ascii_letters, digits, и punctuation.

### Функции:

### `generate_password`

```python
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
```

- **Назначение**: Генерирует случайный пароль на основе предпочтений пользователя.
- **Параметры**: Длина и разрешения для включения букв, цифр и спецсимволов.
- **Возвращает**: Строку сгенерированного пароля.

### `get_user_preferences`

```python
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
```

- **Назначение**: Запрашивает предпочтения пользователя.
- **Возвращает**: Длину и предпочтения пользователя.

### `assess_password_strength`

```python
def assess_password_strength(password):
    length_score = min(1, len(password) // 4)
    char_variety_score = (any(c.islower() for c in password) +
                          any(c.isupper() for c in password) +
                          any(c.isdigit() for c in password) +
                          any(c in string.punctuation for c in password))
    total_score = min(4, length_score + char_variety_score)
    return total_score
```

- **Назначение**: Оценивает сложность пароля.
- **Возвращает**: Оценку от 1 (очень слабый) до 4 (очень сложный).

### `mask_password`

```python
def mask_password(password):
    return '*' * len(password)
```

- **Назначение**: Маскирует пароль звездочками для отображения.
- **Возвращает**: Замаскированную версию пароля.

### `save_password_to_file`

```python
def save_password_to_file(password, filename='passwords.txt'):
    with open(filename, 'a') as file:
        file.write(password + '\n')
```

- **Назначение**: Сохраняет пароль в файл.
- **Параметры**: Пароль и опционально имя файла.
- **Операция**: Добавляет пароль в указанный файл.

## Основная функция

```python
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
```

- **Назначение**: Координирует процесс генерОперациина основе ввода пользователя.
- **Операции**: Собирает предпочтения, генерирует и отображает пароль, оценивает сложность и, при необходимости, сохраняет его.

## Тестирование

### Юнит-тесты

```python
import unittest
from unittest.mock import patch
from main import generate_password, get_user_preferences, save_password_to_file, assess_password_strength, mask_password


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

    def test_save_password_to_file(self):
        test_filename = 'test_passwords.txt'
        test_password = 'test_password'
        save_password_to_file(test_password, test_filename)
        with open(test_filename, 'r') as file:
            lines = file.readlines()
            self.assertIn(test_password + '\n', lines)

    @patch('using_input', return_value=True)
    def test_get_user_preferences(self, mock_input):
        length, use_letters, use_digits, use_specials = get_user_preferences()
        use_digits, use_specials, use_letters = mock_input()
        self.assertIsInstance(length, int)
        self.assertIsInstance(use_digits, bool)
        self.assertIsInstance(use_letters, bool)
        self.assertIsInstance(use_specials, bool)

    if __name__ == '__main__':
        unittest.main()
```

- Назначение: Тестирует каждую функцию для проверки корректности.
- Тесты: 
  - Генерация пароля с проверкой длины и обработки ошибок.
  - Оценка сложности пароля.
  - Маскирование пароля.
  - Сохранение в файл и очистка. 
  - Поверка правильности выбора предпочтений пользователя.

Этот документ предоставляет полное руководство по пониманию и использованию программы генератора паролей.

Проект был сделан как первое итоговое задание 3 модуля специально для BangBangEducation.
