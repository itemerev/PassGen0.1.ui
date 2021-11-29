#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
import win32clipboard
import os
from random import choice, randrange
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


def to_clipboard(data):
    # Функция, копирующая данные в буфер обмена
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()


class PasswordsLibrary:
    library = {}
    def __init__(self):
        with open('results.txt', encoding='utf-8') as results:
            for row in results:
                if row and row[:5] != '    ':
                    self.library[row[:-1]] = []


class App(QWidget):
    def __init__(self):
        super().__init__()

        # Переменные, содержащие символы для генерации пароля
        self.digits = '0123456789'
        self.alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.symbols = '~!@#$%^&*(()+-<>{}[]№?'
        self.special = 'IlO01'

        # Переменные, необходимые для генерации пароля:
        self.num = 3  # Длина пароля в символах
        self.password = ''  # Сгенерированный пароль (по-умолчанию пустая строка)
        self.login = ''  # Сохраненный логин (по-умолчанию пустая строка)
        self.login_password = {}  # Сохраненный словарь - связка логин: пароль (по-умолчанию пустой словарь)
        self.name_login_password = {}  # Сохраненный словарь - связка имя: логин: пароль (по-умолчанию пустой словарь)
        self.library = {}

        self.pass_gen = uic.loadUi('PassGen_Des01.ui')  # Импорт графического интерфейса

        self.start()
        self.click()

    def refresh(self):
        # Метод, который создает библиотеку из файла result.txt
        with open('results.txt', encoding='utf-8') as results:
            name = ''
            for row in results:
                if 'Логин' not in row:
                    name = row[:-2]
                    self.library[name] = []
                else:
                    i = row.index(':')
                    self.library[name].append({row[12:i]:row[i + 11:len(row)-1]})
        print(self.library)

    def start(self):
        # Запускает (показывает) окно приложения
        self.pass_gen.show()
        self.refresh()

    def click(self):
        # Вызывает действие при клике на кнопку
        self.pass_gen.btn_gen.clicked.connect(lambda: self.generate())
        self.pass_gen.btn_enter.clicked.connect(lambda: self.set_num())
        self.pass_gen.btn_login.clicked.connect(lambda: self.set_login())
        self.pass_gen.btn_save.clicked.connect(lambda: self.save_password())
        self.pass_gen.btn_open.clicked.connect(lambda: self.open_data())
        self.pass_gen.btn_add_123.clicked.connect(lambda: self.check_set_123())
        self.pass_gen.btn_add_ABC.clicked.connect(lambda: self.check_set_ABC())
        self.pass_gen.btn_add_abc.clicked.connect(lambda: self.check_set_abc())
        self.pass_gen.btn_add_symbols.clicked.connect(lambda: self.check_set_symbols())

    def open_data(self):
        # Метод, который открывает результирующий файл
        os.startfile('results.txt')

    def save_password(self):
        # Метод, сохраняющий под указанным имененем сгенерированный пароль вместе с логином в файл

        # Введенное имя сохраняется в переменную name, а также в словарь self.name_login_password в качестве ключа к
        # связке "логин: пароль"
        name = self.pass_gen.lineEdit.text()
        self.name_login_password = {name: self.login_password}

        # Сохранение словаря "имя: логин: пароль" в файл
        with open('results.txt', 'a', encoding='utf-8') as save_file:
            print(f'{name}:', file=save_file)
            print(f'    Логин - {self.login}: Пароль - {self.name_login_password.get(name).get(self.login)}',
                  file=save_file)

        self.pass_gen.label.setText('Пароль сохранен в файл')

    def set_login(self):
        # Метод, сохраняющий введеный логин в переменную self.login и в словарь self.login_password "логин: пароль" в
        # качестве ключа к паролю
        self.login = self.pass_gen.lineEdit.text()
        self.login_password = {self.login: self.password}
        self.pass_gen.label.setText('Чтобы сохранить пароль, введите его имя и нажмите SAVE')

    def set_num(self):
        # Метод, задающий длину пароля от 3-х до 18-ти символов
        if self.pass_gen.lineEdit.text().isdigit():  # Проверка, что введенный текст является числом
            self.num = int(self.pass_gen.lineEdit.text())
            if self.num > 18:
                self.num = 18
            if self.num < 3:
                self.num = 3
            if self.num == 3 or self.num == 4:
                self.pass_gen.label.setText(f'Длина пароля {self.num} символа')
            else:
                self.pass_gen.label.setText(f'Длина пароля {self.num} символов')
        else:
            self.pass_gen.label.setText('Введите число от 3-х до 18-ти!')

    def check_set_123(self):
        if self.pass_gen.btn_add_123.isChecked():
            self.pass_gen.btn_123.setChecked(True)

    def check_set_ABC(self):
        if self.pass_gen.btn_add_ABC.isChecked():
            self.pass_gen.btn_ABC.setChecked(True)

    def check_set_abc(self):
        if self.pass_gen.btn_add_abc.isChecked():
            self.pass_gen.btn_abc.setChecked(True)

    def check_set_symbols(self):
        if self.pass_gen.btn_add_symbols.isChecked():
            self.pass_gen.btn_symbols.setChecked(True)

    def generate(self):
        # Метод, генерирующий пароль учитывая включенные кнопки

        # переменная, которые содержит все символы из которых будет генерироваться пароль (по умолчанию пустая строка)
        symbols_to_generate = ''

        # Проверка включенных кнопок для выбора символов из которых будет генерироваться пароль
        if self.pass_gen.btn_123.isChecked():
            symbols_to_generate += self.digits
        if self.pass_gen.btn_ABC.isChecked():
            symbols_to_generate += self.alpha_upper
        if self.pass_gen.btn_abc.isChecked():
            symbols_to_generate += self.alpha_lower
        if self.pass_gen.btn_symbols.isChecked():
            symbols_to_generate += self.symbols
        if not self.pass_gen.btn_special.isChecked():
            temp_sym_to_gen = ''
            for c in symbols_to_generate:
                if c not in self.special:
                    temp_sym_to_gen += c
            symbols_to_generate = temp_sym_to_gen

        # Если переменная, содержащая символы для генерации пароля не пустая, то пароль генерируется
        if symbols_to_generate:
            self.password = ''
            for i in range(self.num):  # Генерируется пароль из заданного количества символов
                self.password += choice(symbols_to_generate)

            # Проверка включенных кнопок для обязательных символов (+), а также наличие обязательных символов в
            # сгенерированном пароле
            if self.pass_gen.btn_add_123.isChecked():  # Для кнопки "123"
                temp = False
                for c in self.password:
                    if c in self.digits:
                        temp = True
                        break

                # Если обязательных символов в пароле нет, то он (обязательный символ) добавляется в конец
                # сгенерированного пароля, удаляя первый символ.
                if not temp:
                    self.password = self.password[1:] + str(randrange(2, 9))

            if self.pass_gen.btn_add_ABC.isChecked():  # Для кнопки "ABC"
                temp = False
                for c in self.password:
                    if c in self.alpha_upper:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('ABCDEFGHJKLMNPRSTUVWXYZ')

            if self.pass_gen.btn_add_abc.isChecked():  # Для кнопки "abc"
                temp = False
                for c in self.password:
                    if c in self.alpha_lower:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('abcdefghijkmnopqrstuvwxyz')

            if self.pass_gen.btn_add_symbols.isChecked():  # Для кнопки "symbols"
                temp = False
                for c in self.password:
                    if c in self.symbols:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('~!@#$%^&*(()+-<>{}[]№?')

            self.pass_gen.lineEdit.setText(self.password)  # Показать пароль в окне lineEdit
            self.pass_gen.label.setText(f'Чтобы задать логин для {self.password}, введите логин и нажмите LOGIN')

            # Копирование сгенерированного пароля в буфер обмена
            to_clipboard(self.password)

        # Если нет нажатых кнопок для выбора символов для генерации пароля, то это выводиться в подсказку
        else:
            self.pass_gen.label.setText(
                'ВЫБЕРИТЕ СИМВОЛЫ!')


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


if __name__ == '__main__':
    main()
