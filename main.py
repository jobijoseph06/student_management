from idlelib.search import SearchDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        #call init of parent class
        super().__init__()
        self.setWindowTitle("Student Management System")
        #menus
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student = QAction("Add Student", self)
        add_student.triggered.connect(self.insert)
        file_menu_item.addAction(add_student)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        edit_action = QAction("Search" , self)
        edit_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_action)

        #creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)

    def load_data(self):

        self.table.setRowCount(0)
        #connect the db
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        for row_numbers, row_data in enumerate(result):
            self.table.insertRow(row_numbers)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_numbers, column_number,QTableWidgetItem(str(data)))
        connection.close()

    #calling the insertdialog class
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

#code to create dialog(another window)
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        #set up the layout
        layout = QVBoxLayout() #class

        #created the student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # created the combo box of subjects
        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Tamil", "Physics" ]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        #add the mobile widget
        self.mobile_num = QLineEdit()
        self.mobile_num.setPlaceholderText("Mobile no:")
        layout.addWidget(self.mobile_num)

        #submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)


        self.setLayout(layout)

    def add_student(self):
        #storing the values from the dialog(name, course, mobile number )
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_num.text()
        #again connect to the DB
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students  (name,course, mobile) VALUES (?, ?, ?) ",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #button
        button  = QPushButton("Search")
        button.clicked.connect(self.search_method)
        layout.addWidget(button)
        self.setLayout(layout)

    #search method
    def search_method(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result  = cursor.execute("SELECT * FROM students WHERE name = ?" ,(name,))
        rows = list(result)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()








#run the application
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())
