# This GUI application converts numbers between ANY bases (2-36)
import os
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,

)

class BaseConverter(QMainWindow):
    """ Constructor - sets up the entire application. """
    def __init__(self):
        super().__init__()
        self.setup_window()

        """ Create all the visual elements we need """

        # Title
        self.title_label = QLabel('Number Base Converter')
        self.title_label.setObjectName('title_label')
        self.title_label.setAlignment(Qt.AlignCenter)

        # Input Section
        self.input_label = QLabel('Enter your number:')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('e.g., 255, FF, 1010, 777...')
        self.input_field.setObjectName('input_field')

        # Error message (hidden at start)
        self.error_message = QLabel()
        self.error_message.setObjectName('error_message')
        self.error_message.hide()

        # Base Selection (2-36)
        self.from_base_label = QLabel('Convert FROM:')
        self.from_base_combo = QComboBox()
        self.from_base_combo.addItems(self.get_all_base_options())
        self.from_base_combo.setCurrentText('10 (Decimal) [0-9]')

        self.to_base_label = QLabel('Convert TO:')
        self.to_base_combo = QComboBox()
        self.to_base_combo.addItems(self.get_all_base_options())
        self.to_base_combo.setCurrentText('2 (Binary) [0-1]')

        # Buttons
        self.convert_button = QPushButton('🔄 Convert')
        self.swap_button = QPushButton('⇄')
        self.swap_button.setMaximumWidth(50)
        self.clear_button = QPushButton('🗑️ Clear All')
        self.copy_button = QPushButton('📋 Copy Result')

        # Result Section
        self.result_label = QLabel('📊 Conversion Results:')
        self.result_label.setObjectName('result_label')
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlainText("🚀 Enter a number and click '🔄 Convert' to see result.")

        self.arrange_layout()
        self.connect_signals()
        self.apply_styles()

    def setup_window(self):
        """ Set up basic window properties """
        self.setWindowTitle('Number Base Converter by Daniel Glover (DTechish)')

        # Handle icon path for both development and bundled executable
        try:
            if hasattr(sys, '_MEIPASS'):
                # Running as bundled executable
                icon_path = os.path.join(sys._MEIPASS, 'icon.png')
            else:
                # Running as script
                icon_path = 'icon.png'

            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                print(f"⚠️  Icon file not found at: {icon_path}")
        except Exception as e:
            print(f"❌ Error loading icon: {e}")

        self.setGeometry(40, 60, 600, 600)

    @staticmethod
    def get_all_base_options():
        """
        Create a complete list of ALL possible number bases (2-36).
        Base 36 uses 0-9 and letters A-Z,so it's the maximum possible base.
        """

        # Bases with their names
        base_names = {
            2: "Binary", 3: "Ternary", 4: "Quaternary", 5: "Quinary",
            6: "Senary", 7: "Septenary", 8: "Octal", 9: "Nonary",
            10: "Decimal", 11: "Undecimal", 12: "Duodecimal", 13: "Tridecimal",
            14: "Tetradecimal", 15: "Pentadecimal", 16: "Hexadecimal",
            17: "Heptadecimal", 18: "Octodecimal", 19: "Enneadecimal",
            20: "Vigesimal", 21: "Unvigesimal", 22: "Duovigesimal",
            23: "Trivigesimal", 24: "Tetravigesimal", 25: "Pentavigesimal",
            26: "Hexavigesimal", 27: "Heptavigesimal", 28: "Octovigesimal",
            29: "Enneavigesimal", 30: "Trigesimal", 31: "Untrigesimal",
            32: "Duotrigesimal", 33: "Tritrigesimal", 34: "Tetratrigesimal",
            35: "Pentatrigesimal", 36: "Hexatrigesimal"
        }

        # Create formatted option for dropdown (combo-box)
        options = []
        for base_num in range(2, 37):  # Starts from 2 to 36
            # formatted string on l01 is default str incase base_num has no value
            base_name = base_names.get(base_num, f"Base-{base_num}")

            # Show which characters each bases uses
            if base_num <= 10:
                chars = f'0-{base_num - 1}'
            else:
                end_letter = chr(ord('A') + base_num - 11)
                chars = f'0-9, A-{end_letter}'

            options.append(f'{base_num} ({base_name}) [{chars}]')

        return options

    def arrange_layout(self):
        """ Arrange all widgets in an organized layout """

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add all sections
        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(20)

        # Input section
        main_layout.addWidget(self.input_label)
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.error_message)
        main_layout.addSpacing(15)

        # Base section
        # Labels row
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(self.from_base_label)
        labels_layout.addSpacing(55)
        labels_layout.addWidget(self.to_base_label)
        main_layout.addLayout(labels_layout)

        # Combo boxes and swap button row
        combos_layout = QHBoxLayout()
        combos_layout.addWidget(self.from_base_combo)
        combos_layout.addWidget(self.swap_button)
        combos_layout.addWidget(self.to_base_combo)
        main_layout.addLayout(combos_layout)

        main_layout.addSpacing(15)

        # buttons in a row
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.copy_button)
        main_layout.addLayout(button_layout)

        main_layout.addSpacing(15)

        # Result section
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.result_display)

    def connect_signals(self):
        """ Connect button clicks to their functions """
        self.convert_button.clicked.connect(self.convert_number)
        self.swap_button.clicked.connect(self.swap_bases)
        self.clear_button.clicked.connect(self.clear_all)
        self.copy_button.clicked.connect(self.copy_result)
        self.input_field.textChanged.connect(self.on_input_text_changed)
        self.input_field.returnPressed.connect(self.convert_number)  # Convert on Enter


    def convert_number(self):
        """ Main conversion method - handles all conversion logic and displays results """
        input_text = self.input_field.text().strip().upper()
        from_base_text = self.from_base_combo.currentText()
        to_base_text = self.to_base_combo.currentText()

        # Get base names for display
        from_base_name = from_base_text.split('(')[1].split(')')[0]
        to_base_name = to_base_text.split('(')[1].split(')')[0]

        # Validate input
        if not self.validate_user_input(input_text):
            return

        if not self.validate_user_base_choice(input_text, from_base_text):
            return

        try:
            # Get the bases in integer form
            from_base_value = int(from_base_text.split()[0])
            to_base_value = int(to_base_text.split()[0])

            # Perform conversion
            if from_base_value == 10:
                result = BaseConverter.convert_from_base10(input_text, to_base_text)
            elif to_base_value == 10:
                result = self.convert_to_base10(input_text, from_base_text)
            else:
                decimal = self.convert_to_base10(input_text, from_base_text)
                result = BaseConverter.convert_from_base10(decimal, to_base_text)

            # Display formatted result
            self.display_result(input_text, result, from_base_value, to_base_value, from_base_name, to_base_name)
        except Exception as e:
            self.show_error(f"Conversion error: {str(e)}")


    def display_result(self, original, result, from_base, to_base, from_name, to_name):
        result_text = f"""✅ CONVERSION SUCCESSFUL!

🔢 Original Number: {original}
📥 From: Base {from_base} ({from_name})
📤 To: Base {to_base} ({to_name})

🎯 RESULT: {result}"""

        self.result_display.setPlainText(result_text)

    def validate_user_input(self, user_input):
        # Validates the number entered by the user
        if not user_input:
            self.show_error('Please enter a number to convert!')
            return False

        if not user_input.isalnum():
            self.show_error('Invalid input! Only letters (A-Z) and digits (0-9) are allowed.')
            return False

        return True

    @staticmethod
    def char_to_base_value(char):
        if char.isdigit():
            # '0' -> 0, '1' -> 1, ..., '9' -> 9
            return int(char)
        else:
            # 'A' -> 10, 'B' -> 11, ..., 'Z' -> 35
            return ord(char) - ord('A') + 10

    @staticmethod
    def base_value_to_char(value):
        if value < 10:
            # 0-9 stay as '0'-'9'
            return str(value)
        else:
            # 10->'A', 11->'B', etc.
            return chr(ord('A') + value - 10)

    def validate_user_base_choice(self, user_input, from_combo):
        # Validates the selected options form the combo box
        end_range = BaseConverter.char_to_base_value(from_combo[-2]) + 1
        valid_range = range(0, end_range)

        for char in user_input:
            char_value = BaseConverter.char_to_base_value(char)
            if char_value not in valid_range:
                # Extract the range part from combo box text like "[0-9, A-L]"
                range_part = from_combo.split(')')
                self.show_error(f'Invalid character "{char}". Please use only the allowed characters for this base: {range_part[1].strip()}')
                return False

        return True

    def convert_to_base10(self, user_input, from_base):
        """Convert from any base to decimal (base 10)"""
        decimal_number = 0
        number_base = from_base.split()[0]

        index = 0
        input_length = len(user_input) - 1
        while index != len(user_input):
            decimal_number += self.char_to_base_value(user_input[index]) * (int(number_base) ** input_length)
            index += 1
            input_length -= 1

        return decimal_number

    @staticmethod
    def convert_from_base10(decimal_number, to_base):
        """Convert from decimal to any base"""
        decimal_number = int(decimal_number)
        if decimal_number == 0:
            return '0'

        number_base = int(to_base.split()[0])
        result = ''

        while decimal_number > 0:
            remainder = decimal_number % number_base
            result += BaseConverter.base_value_to_char(remainder)
            decimal_number //= number_base

        return result[::-1]  # Reverse the string

    def on_input_text_changed(self, text):
        """ Blocks signal temporarily to prevent infinite loop """
        self.input_field.blockSignals(True)
        self.input_field.setText(text.upper())
        self.input_field.blockSignals(False)
        self.clear_error()

    def swap_bases(self):
        """ Swap FROM and TO base selections """
        from_index = self.from_base_combo.currentIndex()
        to_index = self.to_base_combo.currentIndex()

        self.from_base_combo.setCurrentIndex(to_index)
        self.to_base_combo.setCurrentIndex(from_index)

    def clear_all(self):
        """ Reset everything to default state """
        self.input_field.clear()
        self.from_base_combo.setCurrentText('10 (Decimal) [0-9]')
        self.to_base_combo.setCurrentText('2 (Binary) [0-1]')
        self.result_display.setPlainText("🚀 Enter a number and click '🔄 Convert' to see result.")
        self.clear_error()
        self.input_field.setFocus()

        # Clear result state
        self.result_display.setProperty('state', '')
        self.result_display.style().unpolish(self.result_display)
        self.result_display.style().polish(self.result_display)

    def copy_result(self):
        """ Copy the conversion result to clipboard """
        result_text = self.result_display.toPlainText()
        if "RESULT:" in result_text:
            result_only = result_text.split(':')[-1]
            QApplication.clipboard().setText(result_only)

            # Show temporary feedback
            self.copy_button.setText('✅ Copied!')

            # Restore after 1.5 seconds
            QTimer.singleShot(1500, lambda: self.copy_button.setText('📋 Copy Result'))
            QApplication.processEvents()
        else:
            self.show_error("No result to copy! Please convert a number first.")

    def show_error(self, message):
        """ Displays error message to user """
        self.error_message.setText(f"⚠️ {message}")
        self.error_message.show()

    def clear_error(self):
        """ Hide error message """
        self.error_message.hide()

    def apply_styles(self):
        """Load styling from external CSS file"""
        try:
            # Get the correct path for the bundled executable
            if hasattr(sys, '_MEIPASS'):
                # Running as bundled executable
                css_path = os.path.join(sys._MEIPASS, 'styles.qss')
            else:
                # Running as script
                css_path = 'styles.qss'

            with open(css_path, 'r') as style_file:
                stylesheet = style_file.read()
                self.setStyleSheet(stylesheet)
                print("✅ Stylesheet loaded successfully!")
        except FileNotFoundError:
            print("⚠️  Warning: styles.qss file not found. Using default styling.")
            print("💡 Create a styles.qss file in the same folder for custom styling.")
        except Exception as e:
            print(f"❌ Error loading stylesheet: {e}")
            print("🔄 Using default styling instead.")


""" Application starts here """
def main():
    # Create Qt Application
    app = QApplication(sys.argv)

    # Create and show our converter
    converter = BaseConverter()
    converter.show()

    # Starts the application loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
