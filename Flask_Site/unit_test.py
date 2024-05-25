import json
import unittest
from app import app, write_to_file, read_from_file
from unittest.mock import patch

name = 'Clancy'
class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_page(self):
        response = self.app.get('/')
        self.assertIn('Анкета Bandito', response.data.decode('utf-8'))

    def test_user_form_submission(self):
        with patch('app.write_to_file') as mock_write_to_file:
            age = 23
            email = 'Trech@NoChances.com'

            # Отправляем POST запрос на главную страницу
            self.app.post('/', data=dict(name=name, age=age, email=email), follow_redirects=True)

            # Затем отправляем GET запрос на страницу успеха
            response = self.app.get(f'/complete?name={name}&age={age}&email={email}', follow_redirects=True)

            # Проверяем, что страница успешно загружена после перенаправления
            self.assertEqual(response.status_code, 200)

            # Проверяем, что функция write_to_file была вызвана с правильными аргументами
            write_to_file({'name': name, 'age': age, 'email': email})

            # Проверяем, что данные записались в файл
            with open('users_data.json', 'r', encoding='utf-8') as file:
                last_data = read_from_file()
                self.assertEqual({'name': name, 'age': age, 'email': email}, last_data)

    def test_complete_page(self):
        response = self.app.get('/complete?name=Clancy&age=23&email=Trech@NoChances.com')
        # Проверяем, что имя пользователя отображается на странице успеха
        self.assertIn(f'Спасибо, {name}, ваша анкета успешно отправлена!', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()