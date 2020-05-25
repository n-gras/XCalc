from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextFieldRect

from operator import pow, truediv, mul, add, sub, neg

from decimal import Decimal  # uses decimal module to make simple calculator 
# without floating point rounding errors

import re

operators = {
        ' + ': add,
        ' - ': sub,
        ' / ': truediv,
        ' * ': mul,
        '^': pow,
        '-': neg
}


class MainApp(MDApp):
    def build(self):
        self.operators = ["^", " / ", " * ", " + ", " - "]
        # operators /,*,+,- are added with leading and trailing space to make
        # identification possible between that and negative numbers
        self.last_was_operator = None
        self.last_button = None
        main_layout = MDBoxLayout(orientation="vertical")
        self.solution = MDTextFieldRect(
            multiline=False,
            readonly=True,
            size_hint=[1, None],
            halign="right",
            height="80sp",
            font_size='55sp'
        )
        main_layout.add_widget(self.solution)
        buttons = [
            ["", "C", "<-", "^"],
            ["", "", "", " / "],
            ["7", "8", "9", " * "],
            ["4", "5", "6", " - "],
            ["1", "2", "3", " + "],
            ["+/-", "0", ".", "="]
        ]
        for row in buttons:
            h_layout = MDBoxLayout()
            for label in row:
                button = MDRectangleFlatButton(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint=(1, 1),
                    font_size='20sp'
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        operator_split = re.split(r"(\s[*/+-]\s|\^)", current)  # split solution
        # text into different groups per operator to for check decimal
        # separator below
        print(operator_split)
        last_split = str(operator_split[-1])  # get last entered operator group
        print(last_split)

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        elif button_text == "<-":
            new_text = current[:-1]
            self.solution.text = new_text
        elif button_text == "=":
            if current != "" and current != ".":
                # solution = str(eval(self.solution.text))
                # self.solution.text = solution
                self.solution.text = str(calculate(current))
            else:
                return

        elif button_text == "+/-":
            if last_split == "":
                new_split = "-"
            elif last_split == "-":
                new_text = current[:-1]
                self.solution.text = new_text
                return
            else:
               new_split = [-Decimal(last_split)]

            if len(operator_split) > 1:
                self.solution.text = ''.join(operator_split[:-1]) \
                 + str(new_split[0])
            else:
                self.solution.text = str(new_split[0])

        else:
            if current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            elif current and last_split == "" and (operator_split[-2] in self.operators
                                        and button_text in self.operators):
                # Don't add two operators right after each other,
                # instead replace operator
                new_text = ''.join(operator_split[:-2]) + button_text
                self.solution.text = new_text
                return
            elif (current and last_split.find(".") != -1
                  and button_text == "."):
                # check if decimal separator was already entered- first
                # turn number after last operator into string to use find
                # function
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators


def calculate(x):
    if isDigit(x):
        return Decimal(x)
    for each in operators.keys():
        left, operator, right = x.partition(each)
        if operator in operators:
            return operators[operator](calculate(left), calculate(right))


def isDigit(x):
    return x.replace('.', '').replace('-', '').isdigit()


if __name__ == "__main__":
    app = MainApp()
    app.run()
