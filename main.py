from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition


class MHintTextInput(TextInput):
    hint_text = StringProperty("Задайте массу...")

    def __init__(self, **kwargs):
        super(MHintTextInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus)
        self.color = (0.5, 0.5, 0.5, 1)  # Цвет текста подсказки
        self.text = self.hint_text  # Установка текста подсказки
        self.multiline = False  # Убедитесь, что это значение False для однострочного ввода
        self.halign = 'center'  # Устанавливаем выравнивание по центру

    def on_focus(self, instance, value):
        if value:  # Фокус на текстовом поле
            if self.text == self.hint_text:
                self.text = ''
                self.color = (1, 1, 1, 1)  # Белый цвет текста
        else:  # Убираем текст подсказки, если поле пустое
            if self.text == '':
                self.text = self.hint_text
                self.color = (0.5, 0.5, 0.5, 1)  # Серый цвет подсказки

class LHintTextInput(TextInput):
    hint_text = StringProperty("Задайте расстояние...")

    def __init__(self, **kwargs):
        super(LHintTextInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus)
        self.color = (0.5, 0.5, 0.5, 1)
        self.text = self.hint_text
        self.multiline = False  # Убедитесь, что это значение False для однострочного ввода
        self.halign = 'center'  # Устанавливаем выравнивание по центру

    def on_focus(self, instance, value):
        if value:
            if self.text == self.hint_text:
                self.text = ''
                self.color = (1, 1, 1, 1)
        else:
            if self.text == '':
                self.text = self.hint_text
                self.color = (0.5, 0.5, 0.5, 1)

class Cube(Widget):
    mass = NumericProperty(0)

    def __init__(self, mass, label_text, **kwargs):
        super(Cube, self).__init__(**kwargs)
        self.mass = mass
        self.x = Window.width
        print(self.x)
        self.y = Window.height
        print(self.y)
        self.a = self.x * self.y / ((self.x+self.y))
        self.size = (self.x * self.y / ((self.x+self.y)*9.36), self.x * self.y / ((self.x+self.y)*8))
        self.image = Image(source="weight.png", size=self.size)
        self.add_widget(self.image)  # Очищаем предыдущий холст
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.label = Label(text=label_text, color=(0, 0, 0, 1), font_size=(self.a/28), size_hint=(None, None), size=(self.size[0], self.size[1] / 4))
        self.add_widget(self.label)

    def update_rect(self, *args):
        # self.x = Window.width / 2 -10
        self.y = Window.height / 2 * 0.68 - self.a / 10
        self.image.pos = self.pos
        self.label.pos = self.pos[0], self.pos[1] + self.a/36
        print(self.size)

class LineWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(LineWidget, self).__init__(**kwargs)

        # Используем Canvas для рисования линии
        with self.canvas:
            Color(0, 0, 0)  # Черный цвет
            self.line = Line(points=[0, 0, 0, 0], width=2)  # Инициализация с нулевыми координатами

        # Привязываем метод на изменение размера
        self.bind(size=self.draw_line)

        self.cubes = []  # Список кубиков

    def draw_line(self, *args):
        # Обновляем координаты линии в зависимости от ширины и высоты виджета
        self.line_y = self.height / 2
        self.canvas.clear()  # Очищаем текущий холст
        with self.canvas:
            Color(0.18, 0.21, 0.29)  # красный цвет
            Line(points=[self.width / 3, self.line_y, self.width, self.line_y], width=2)

    def add_cube(self, mass, position, label_text):
        # Добавляем кубик на линию
        cube = Cube(mass=mass, label_text=label_text)
        cube.pos = (position, self.height / 2 - cube.height / 2)  # Центрируем кубик по вертикали
        self.add_widget(cube)
        self.cubes.append(cube)


# Определяем второй экран
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.x = Window.width
        self.y = Window.height
        self.a = self.x * self.y / (self.x + self.y)
        layout = AnchorLayout()
        label = Label(text='Это второй экран', font_size=40)
        fl = FloatLayout()
        back_button = Button(
            background_normal="close.png",
            background_down="close_pressed.png",
            size_hint=(None, None),
            size=(self.size[0]/1.2, self.size[1]/1.2),
            pos=(self.x - self.a/5, self.y - self.a/5)  # Устанавливаем обработчик нажатия
        )
        back_button.bind(on_release=self.go_back)
        fl.add_widget(back_button)
        layout.add_widget(fl)
        layout.add_widget(label)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = NoTransition()
        self.manager.current = 'main'  # Переключаемся обратно на основной экран


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.leftlist1 = []  # Списки для хранения весов
        self.leftlist2 = []
        self.rightlist1 = []
        self.rightlist2 = []
        self.centerw = 0
        self.x = Window.width
        self.y = Window.height
        self.size = (self.x * self.y / ((self.x + self.y) * 3.5), self.x * self.y / ((self.x + self.y) * 3.5))

        Window.clearcolor = (0.91,0.90,0.99, 1)
        layout = AnchorLayout()

        self.line_widget = LineWidget(size_hint=(0.75, 0.68))  # Высота линии 0.75, 0.68
        layout.add_widget(self.line_widget)

        center_button = FloatLayout()
        add_button = Button(
            background_normal="button2.png",
            background_down="button2_pressed.png",
            text="груз для выравнивания",
            size_hint=(0.3, 0.1),
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            on_release=self.center_add_weight  # Устанавливаем обработчик нажатия
        )
        center_button.add_widget(add_button)

        # Создаем текстовые поля для ввода чисел
        self.centerinput1 = MHintTextInput(hint_text_color=(0, 0, 0, 0.5), background_normal="button.png", background_active="button_pressed.png",
                                           foreground_color=(0, 0, 0, 1), cursor_color=(0.97, 0.97, 0.99, 1), border=(20, 20, 20, 20), size_hint=(0.3, 0.1),
                                           height=40, pos_hint={'center_x': 0.5, 'center_y': 0.8})
        center_button.add_widget(self.centerinput1)
        self.centerinput2 = LHintTextInput(hint_text_color=(0, 0, 0, 0.5), background_normal="button.png", background_active="button_pressed.png",
                                           foreground_color=(0, 0, 0, 1), cursor_color=(0.97, 0.97, 0.99, 1), border=(20, 20, 20, 20), size_hint=(0.3, 0.1),
                                           height=40, pos_hint={'center_x': 0.5, 'center_y': 0.699})
        center_button.add_widget(self.centerinput2)

        # Добавляем правую кнопку в Layout
        layout.add_widget(center_button)

        end_button = FloatLayout()
        add_button = Button(
            background_normal="button2.png",
            background_down="button2_pressed.png",
            text="вычислить",
            size_hint=(0.2, 0.1),
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            on_release=self.calculate  # Обработчик нажатия
        )
        end_button.add_widget(add_button)
        layout.add_widget(end_button)

        right_button = FloatLayout()
        add_button = Button(
            background_normal="button2.png",
            background_down="button2_pressed.png",
            text="Добавить груз справа",
            size_hint=(0.25, 0.1),
            height=50,
            pos_hint={'center_x': 0.88, 'center_y': 0.9},
            on_release=self.right_add_weight  # Устанавливаем обработчик нажатия
        )
        right_button.add_widget(add_button)
        # Создаем текстовые поля для ввода чисел
        self.rightinput1 = MHintTextInput(hint_text_color=(0, 0, 0, 0.5), background_normal="button.png", background_active="button_pressed.png",
                                          foreground_color=(0, 0, 0, 1), cursor_color=(0.97, 0.97, 0.99, 1), border=(20, 20, 20, 20), size_hint=(0.25, 0.1),
                                          height=40, pos_hint={'center_x': 0.88, 'center_y': 0.8})
        right_button.add_widget(self.rightinput1)
        self.rightinput2 = LHintTextInput(hint_text_color=(0, 0, 0, 0.5), background_normal="button.png", background_active="button_pressed.png",
                                          foreground_color=(0, 0, 0, 1), cursor_color=(0.97, 0.97, 0.99, 1), border=(20, 20, 20, 20),size_hint=(0.25, 0.1),
                                          height=40, pos_hint={'center_x': 0.88, 'center_y': 0.699})
        right_button.add_widget(self.rightinput2)
        # Добавляем правую кнопку в Layout
        layout.add_widget(right_button)

        left_button = FloatLayout()
        add_button = Button(
            background_normal="button2.png",
            background_down="button2_pressed.png",
            text="Добавить груз слева",
            size_hint=(0.25, 0.1),
            height=50,
            pos_hint={'center_x': 0.12, 'center_y': 0.9},
            on_release=self.left_add_weight  # Устанавливаем обработчик нажатия
        )
        left_button.add_widget(add_button)
        # Создаем текстовые поля для ввода чисел
        self.leftinput1 = MHintTextInput(hint_text_color=(0, 0, 0, 0.5), background_normal="button.png", background_active="button_pressed.png",
                                         foreground_color=(0, 0, 0, 1), cursor_color=(0.97, 0.97, 0.99, 1), border=(20, 20, 20, 20), size_hint=(0.25, 0.1),
                                         height=40, pos_hint={'center_x': 0.12, 'center_y': 0.8})
        left_button.add_widget(self.leftinput1)
        self.leftinput2 = LHintTextInput(hint_text_color=(0, 0, 0, 0.5), background_normal="button.png", background_active="button_pressed.png",
                                         foreground_color=(0, 0, 0, 1), cursor_color=(0.97, 0.97, 0.99, 1), border=(20, 20, 20, 20), size_hint=(0.25, 0.1),
                                         height=40, pos_hint={'center_x': 0.12, 'center_y': 0.699})
        left_button.add_widget(self.leftinput2)
        # Добавляем левую кнопку в Layout
        layout.add_widget(left_button)

        img = FloatLayout()  # Изображение треугольника
        triangle = Image(
            source='triangle.png',
            size_hint=(1, 0.19),
            pos_hint={'center_x': 0.5, 'center_y': 0.26}
        )
        img.add_widget(triangle)
        layout.add_widget(img)  # Добавляем изображение в Layout

        self.line_widget = LineWidget(size_hint=(0.75, 0.68))  # Высота линии 0.75, 0.68
        layout.add_widget(self.line_widget)

        fl = FloatLayout()
        switch_button = Button(
            background_normal="question.png",
            background_down="question_pressed.png",
            size_hint=(None, None),
            size=self.size,
            pos_hint={'center_x': 0.9, 'center_y': 0.1}  # Устанавливаем обработчик нажатия
        )
        switch_button.bind(on_release=self.switch_to_second_screen)
        fl.add_widget(switch_button)
        layout.add_widget(fl)

        self.add_widget(layout)

    def calculate(self, instance):
        # Логика обработки Момента силы рычага
        if len(self.leftlist1) != len(self.leftlist2) or len(self.rightlist1) != len(self.rightlist2):
            self.threeshow_popup(instance)
            return
        self.leftresult = sum(a * b for a, b in zip(self.leftlist1, self.leftlist2))
        self.rightresult = sum(a * b for a, b in zip(self.rightlist1, self.rightlist2))
        print("Результат лево:", self.leftresult)
        print("результат право:", self.rightresult)
        if self.leftresult > self.rightresult:
            print("рычаг перевешивает на лево")
            self.result = (self.leftresult - self.rightresult) / self.centerw
        if self.leftresult < self.rightresult:
            print("рычаг перевешивает на право")
            self.result = (self.rightresult - self.leftresult) / self.centerw
        if self.leftresult == self.rightresult:
            self.result = 0
            print("рычаг в равновесии")
        var = int(self.result)
        if var == self.result:
            self.result = var
            print(self.result)
            self.threershow_popup(instance)
        else:
            self.threershow_popup(instance)

    def left_add_weight(self, instance, *args):
        self.xx = Window.width
        self.yy = Window.height
        left_weight1 = self.leftinput1.text
        left_weight2 = self.leftinput2.text
        left_weight = left_weight1
        try:
            left_weight1 = float(left_weight1)
            left_weight2 = float(left_weight2)
            self.leftlist1.append(left_weight1)
            self.leftlist2.append(left_weight2)
            position = ((self.xx / 2 - (self.xx * self.yy / ((self.xx+self.yy)*19))) - ((left_weight2) * (self.xx / 400)))  # Положение кубика на линии
            self.line_widget.add_cube(left_weight1, position, f"{left_weight}")
            print(f"Добавляем груз слева: {left_weight1}, {left_weight2}")
            print(self.xx)
        except ValueError:
            self.twoshow_popup(instance)

    def right_add_weight(self, instance):
        self.xx = Window.width
        self.yy = Window.height
        right_weight1 = self.rightinput1.text
        right_weight2 = self.rightinput2.text
        right_weight = right_weight1
        try:
            right_weight1 = float(right_weight1)
            right_weight2 = float(right_weight2)
            self.rightlist1.append(right_weight1)
            self.rightlist2.append(right_weight2)
            position = ((self.xx / 2 - (self.xx * self.yy / ((self.xx+self.yy)*19))) + ((right_weight2) * (self.xx / 400)))  # Положение кубика на линии
            self.line_widget.add_cube(right_weight1, position, f"{right_weight}")
            print(f"Добавляем груз справа: {right_weight1}, {right_weight2}")
        except ValueError:
            self.twoshow_popup(instance)

    def center_add_weight(self, instance):
        self.center_weight1 = str(self.centerinput1.text)
        self.center_weight2 = str(self.centerinput2.text)

        if self.center_weight1 == "Задайте массу..." or self.center_weight2 == "Задайте расстояние...":
            try:
                self.center_weight1 = float(self.center_weight1)
                self.centerw = float(self.center_weight1)
            except ValueError:
                try:
                    self.center_weight2 = float(self.center_weight2)
                    self.centerw = float(self.center_weight2)
                except ValueError:
                    self.twoshow_popup(instance)
        else:
            self.oneshow_popup(instance)
        print(f"центр: {self.centerw}")

    def threershow_popup(self, instance):
        self.result = str(self.result)
        if len(self.result) > 5:
            self.result = float(self.result[0] + self.result[1] + self.result[2] + self.result[3])
        popup_content = FloatLayout()
        if self.leftresult > self.rightresult:
            a = str("справа")
        elif self.leftresult < self.rightresult:
            a = str("слева")
        if self.leftresult != self.rightresult:
            if self.center_weight2 == "Задайте расстояние...":
                popup_label = Label(text=f"добавьте груз на расстоянии {self.result} {a}!", size_hint=(0.8, 0.2),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.7})
                close_button = Button(text="Ок", size_hint=(0.6, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.3})
            elif self.center_weight1 == "Задайте массу...":
                popup_label = Label(text=f"добавьте груз массой {self.result} {a}!", size_hint=(0.8, 0.2),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.7})
                close_button = Button(text="Ок", size_hint=(0.6, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        else:
            popup_label = Label(text="рычаг в равновесии", size_hint=(0.8, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.7})
            close_button = Button(text="Ок", size_hint=(0.6, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.3})

        popup_content.add_widget(popup_label)
        popup_content.add_widget(close_button)
        popup = Popup(title="Новое окно",
                      content=popup_content,
                      size_hint=(0.8, 0.5),
                      auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def twoshow_popup(self, instance):
        popup_content = FloatLayout()
        popup_label = Label(text="Введите числа", size_hint=(0.8, 0.2),
                            pos_hint={'center_x': 0.5, 'center_y': 0.7})
        close_button = Button(text="Ок", size_hint=(0.6, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.3})

        popup_content.add_widget(popup_label)
        popup_content.add_widget(close_button)

        popup = Popup(title="Новое окно",
                      content=popup_content,
                      size_hint=(0.8, 0.5),
                      auto_dismiss=False)

        close_button.bind(on_press=popup.dismiss)

        popup.open()

    def oneshow_popup(self, instance):
        popup_content = FloatLayout()
        popup_label = Label(text="Введите одно значение", size_hint=(0.8, 0.2),
                            pos_hint={'center_x': 0.5, 'center_y': 0.7})
        close_button = Button(text="Ок", size_hint=(0.6, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.3})

        popup_content.add_widget(popup_label)
        popup_content.add_widget(close_button)

        popup = Popup(title="Новое окно",
                      content=popup_content,
                      size_hint=(0.8, 0.5),
                      auto_dismiss=False)

        close_button.bind(on_press=popup.dismiss)

        popup.open()


    def switch_to_second_screen(self, instance):
        self.manager.transition = FadeTransition(clearcolor=(0.91,0.90,0.99))
        self.manager.current = 'second'  # Переключаемся на второй экран


class MainApp(App):
    def build(self):

        sm = ScreenManager()  # Создаем ScreenManager
        sm.add_widget(MainScreen(name='main'))  # Добавляем основной экран
        sm.add_widget(SecondScreen(name='second'))  # Добавляем второй экран
        return sm  # Возвращаем ScreenManager


if __name__ == '__main__':
    MainApp().run()  # Запуск приложения
