from idlelib.search import SearchDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
import sys
import sqlite3

from PyQt6.sip import delete


class MainWindow(QMainWindow):
    def __init__(self):
        #call init of parent class
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)
        #menus
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student.triggered.connect(self.insert)
        file_menu_item.addAction(add_student)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        edit_action = QAction(QIcon("icons/search.png"),"Search" , self)
        edit_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_action)

        #creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)

        #toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student)
        toolbar.addAction(edit_action)

        #status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        #detect the cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        #find push button
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)


        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()




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
        cursor.execute("SELECT * FROM students WHERE name = ?" ,(name,))
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # set up the layout
        layout = QVBoxLayout()  # class

        #returns the selected cell student_name
        index = main_window.table.currentRow()

        #get id from selected rows
        self.student_id = main_window.table.item(index, 0).text()

        #extracting the name from the column
        student_name = main_window.table.item(index, 1).text()



        # created the student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #extracting the course
        course_name= main_window.table.item(index, 2).text()
        # created the combo box of subjects
        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Tamil", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # add the mobile widget
        mobile_num = main_window.table.item(index, 3).text()
        self.mobile_num = QLineEdit(mobile_num)
        self.mobile_num.setPlaceholderText("Mobile no:")
        layout.addWidget(self.mobile_num)

        # submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update)
        layout.addWidget(button)

        self.setLayout(layout)

    def update(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?,course = ?, mobile = ? WHERE  id = ? ",
                       (self.student_name.text(), self.course_name.currentText(), self.mobile_num.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()



class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")


        #widgets
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("yes")
        no = QPushButton("no")

        #add widgets to the layout

        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)

        self.setLayout(layout)

        #connect the button to method
        yes.clicked.connect(self.delete_data)

    def delete_data(self):
        # returns the selected cell student_name
        index = main_window.table.currentRow()

        # get id from selected rows
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()

        #reload
        main_window.load_data()
        #close the window
        self.close()

        confirm_message = QMessageBox()
        confirm_message.setWindowTitle("Success")
        confirm_message.setText("The record was deleted successfully!")
        confirm_message.exec()


#run the application
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())
