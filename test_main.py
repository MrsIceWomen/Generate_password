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
