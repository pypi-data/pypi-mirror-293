##! 
##! Copyright(c) 2022, 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import sys
import math

from srsgui.ui.qt.QtCore import Qt, Signal
from srsgui.ui.qt.QtWidgets import QApplication, QWidget, QSpinBox, QDoubleSpinBox, \
                                   QLabel, QFormLayout, QWidget, QPushButton, \
                                   QHBoxLayout, QSpacerItem, QSizePolicy


class IntegerSpinBox(QSpinBox):
    """
    Adjust step size depending on the cursor position
    """

    def stepBy(self, steps):
        prefix_len = len(self.prefix())
        suffix_len = len(self.suffix())
        min_pos = prefix_len + 1 if self.value() < 0 else prefix_len

        text = self.lineEdit().text()
        cur_pos = self.lineEdit().cursorPosition()
        sep_pos = len(text) - suffix_len

        if cur_pos < min_pos:
            return

        exponent = sep_pos - cur_pos

        single_step = 10 ** exponent
        self.setSingleStep(single_step)

        super().stepBy(steps)

        self.lineEdit().deselect()

        min_pos = prefix_len + 1 if self.value() < 0 else prefix_len

        text = self.lineEdit().text()
        new_sep_pos = len(text) - suffix_len

        new_cur_pos = cur_pos + new_sep_pos - sep_pos
        if new_cur_pos < min_pos:
            new_cur_pos = min_pos
        self.lineEdit().setCursorPosition(new_cur_pos)


class FloatSpinBox(QDoubleSpinBox):
    """
    Adjust step size depending on the cursor position
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimum_step = 0.1
        self.significant_figures = 4
        self.precision = 3
        self.decis = 3
        self.setDecimals(10)

    def set_minimum_step(self, value):
        self.minimum_step = value
        step = self.minimum_step if self.minimum_step > 1e-12 else 1e-12
        self.decis = math.ceil(-math.log10(step))

    def set_significant_figures(self, value):
        self.significant_figures = value

    def valueFromText(self, text):
        try:
            if self.suffix():
                unit_len = len(self.suffix())
                value = float(text[:-unit_len])

            else:
                value = float(text)
            if value < self.minimum():
                value = self.minimum()
            elif value > self.maximum():
                value = self.maximum()
        except ValueError:
            print('valueFromText ValueError', text, self.suffix())
            value = self.minimum()
        return value

    def textFromValue(self, value):
        prec = self.decis
        try:
            if abs(value) < self.minimum_step:
                return '0.0'

            digits = math.ceil(math.log10(abs(value)))
            """
            if digits == self.significant_figures:
                step = 1
            else:
                step = 10 ** (digits - self.significant_figures)
            value = round(value / step) * step
            """
            if digits > -3:
                prec = self.significant_figures - digits
                prec = self.decis if prec > self.decis else prec
                prec = 0 if prec < 0 else prec
                self.precision = prec
                format_string = '{:.' + str(prec) + 'f}'
            else:
                format_string = '{:.' + str(self.significant_figures - 1) + 'e}'

            text = format_string.format(value)
        except Exception as e:
            print('Error in textFromValue: {}'.format(e))
            return ''
        return text

    def stepBy(self, steps):
        prefix_len = len(self.prefix())
        suffix_len = len(self.suffix())
        min_pos = prefix_len + 1 if self.value() < 0 else prefix_len

        text = self.lineEdit().text().lower()
        cur_pos = self.lineEdit().cursorPosition()
        max_pos = len(text) - suffix_len

        if cur_pos < min_pos or cur_pos > max_pos:
            return

        e_pos = text.find('e')
        if e_pos > 0 and e_pos < cur_pos:  # cursor is on the right side of 'E'
            return

        exponent = 0
        if 0 < e_pos < max_pos:
            try:
                exponent = int(text[e_pos + 1: max_pos])
            except:
                return

        sep_pos = text.find('.')
        if sep_pos < 0:
            sep_pos = len(text) - suffix_len

        exponent += sep_pos - cur_pos
        if exponent == -1:
            cur_pos += 1

        if exponent < -1:
            exponent += 1

        single_step = 10 ** exponent
        self.setSingleStep(single_step)

        super().stepBy(steps)

        self.lineEdit().deselect()

        min_pos = prefix_len + 1 if self.value() < 0 else prefix_len

        text = self.lineEdit().text()
        new_sep_pos = text.find('.')
        if new_sep_pos < 0:
            new_sep_pos = len(text) - suffix_len

        new_cur_pos = cur_pos + new_sep_pos - sep_pos
        if new_cur_pos < min_pos:
            new_cur_pos = min_pos
        self.lineEdit().setCursorPosition(new_cur_pos)


class RunButton(QWidget):
    pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, -1, 1)
        self.button = QPushButton('Run', self)
        spacer = QSpacerItem(100, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.button)
        layout.addItem(spacer)
        self.button.pressed.connect(self.pressed)
