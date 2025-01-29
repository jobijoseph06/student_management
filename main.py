from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        #call init of parent class
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student = QAction("Add Student", self)
        file_menu_item.addAction(add_student)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        #creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)

    def load_data(self):
        #connect the db
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        for row_numbers, row_data in enumerate(result):
            self.table.insertRow(row_numbers)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_numbers, column_number,QTableWidgetItem(str(data)))
        connection.close()


#run the application
app = QApplication(sys.argv)
app_calculator = MainWindow()
app_calculator.load_data()
app_calculator.show()
sys.exit(app.exec())
