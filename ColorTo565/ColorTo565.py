import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QColorDialog, QLabel
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

def rgb_to_rgb565(r, g, b):
    """
    Преобразует 8-битный RGB (0-255) в 16-битный формат RGB565.
    Формат: 5 бит для красного, 6 бит для зелёного, 5 бит для синего.
    """
    r5 = r >> 3       # Отбрасываем 3 младших бита у красного
    g6 = g >> 2       # Отбрасываем 2 младших бита у зелёного
    b5 = b >> 3       # Отбрасываем 3 младших бита у синего
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    return rgb565

class ClickableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Дополнительное свойство для хранения чистой hex-строки (например, "0x46AC")
        self.hex_value = ""

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.hex_value:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.hex_value)
                print("Скопировано в буфер обмена:", self.hex_value)
        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Picker to RGB565")
        self.resize(300, 200)
        
        # Кнопка для выбора цвета
        self.button = QPushButton("Выбрать цвет")
        self.button.clicked.connect(self.choose_color)
        
        # ClickableLabel для вывода результата, с возможностью копирования
        self.label = ClickableLabel("Цвет: Не выбран")
        self.label.setStyleSheet("font-size: 18px; padding: 10px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Располагаем элементы вертикально
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def choose_color(self):
        # Открываем диалог выбора цвета
        color = QColorDialog.getColor()
        if color.isValid():
            r = color.red()
            g = color.green()
            b = color.blue()
            # Преобразуем в RGB565
            rgb565 = rgb_to_rgb565(r, g, b)
            # Форматируем вывод в шестнадцатеричном виде (например, "0x46AC")
            hex_str = f"0x{rgb565:04X}"
            # Сохраняем чистое значение hex для копирования
            self.label.hex_value = hex_str
            # Обновляем текст метки (можно оставить только hex_str, если нужно)
            self.label.setText(f"Выбранный цвет: {hex_str}")
            # Устанавливаем фон метки равным выбранному цвету
            self.label.setStyleSheet(
                f"font-size: 18px; padding: 10px; background-color: {color.name()};"
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
