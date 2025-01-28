from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
from datetime import datetime
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        # Call the __init__ function of the parent class (QWidget)
        super().__init__()

        # Set up grid layout
        grid = QGridLayout()

        # Create labels and input fields
        self.name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_label = QLabel("Date of Birth MM/DD/YYYY:")
        self.date_line_edit = QLineEdit()

        # Create the calculate button
        cal_button = QPushButton("Calculate Age")
        # Connect button to the find_age function
        cal_button.clicked.connect(self.find_age)

        # Create the result label
        self.result_label = QLabel("")

        # Add widgets to the grid
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)
        grid.addWidget(cal_button, 2, 0, 1, 2)
        grid.addWidget(self.result_label, 3, 0, 1, 2)

        # Set the layout for the widget
        self.setLayout(grid)

    # Function to calculate age
    def find_age(self):
        try:
            # Get the current year
            current_year = datetime.now().year

            # Get the date of birth from the input field
            date_of_birth = self.date_line_edit.text()

            # Parse the date of birth
            birth_date = datetime.strptime(date_of_birth, "%m/%d/%Y")
            year_of_birth = birth_date.year

            # Calculate the age
            age = current_year - year_of_birth

            # Display the result
            name = self.name_line_edit.text()
            self.result_label.setText(f"{name} is {age} years old.")
        except ValueError:
            # Handle invalid date format
            self.result_label.setText("Invalid date format. Please use MM/DD/YYYY.")


# Run the application
app = QApplication(sys.argv)
app_calculator = AgeCalculator()
app_calculator.show()
sys.exit(app.exec())
