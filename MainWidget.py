'''
Created on May 23, 2019

@author: amin
'''

from PyQt5.QtWidgets import (QPushButton, QPlainTextEdit, QVBoxLayout,
                             QHBoxLayout, QWidget, QGridLayout, QInputDialog,
                             QLineEdit, QMessageBox, QSizePolicy)

from PyQt5.QtGui import QColor
from Notebook import Notebook
from Note import Note
from Section import Section


class MainWidget(QWidget):
    def __init__(self):
        self.layout = None
        self.notebook = Notebook()
        self.notebook.add_section(Section('پیش فرض'))
        self.show_login_page()

    @staticmethod
    def quit_app():
        exit()

    def show_login_page(self): 
        QWidget.__init__(self)

        # login button
        login = QPushButton("ورود")
        login.setSizePolicy(QSizePolicy.Preferred,
                            QSizePolicy.Preferred)
        login.setStyleSheet("background-color: rgb(228, 210, 86)")
 
        # sign up button
        signup = QPushButton("ثبت نام")
        signup.setSizePolicy(QSizePolicy.Preferred,
                             QSizePolicy.Preferred)
        signup.setStyleSheet("background-color: rgb(228, 210, 86)")
 
        # exit button
        ex = QPushButton("خروج")
        ex.setSizePolicy(QSizePolicy.Preferred,
                         QSizePolicy.Preferred)
        ex.setStyleSheet("background-color: rgb(228, 210, 86)")
 
        # set layout
        self.layout = QGridLayout()
        self.layout.setRowStretch(0, 10)
        self.layout.setRowStretch(1, 10)
        self.layout.setRowStretch(2, 5)
        self.layout.addWidget(login, 0, 2)
        self.layout.addWidget(signup, 1, 2)
        self.layout.addWidget(ex, 2, 0)
        self.layout.setSpacing(100)
        self.setLayout(self.layout)
 
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(78, 143, 171))
        self.setPalette(p)
         
        # Connecting the signal
        login.clicked.connect(self.handle_login)
        signup.clicked.connect(self.handle_signup)
        ex.clicked.connect(self.quit_app)

    def get_text(self, widget_name, widget_text):
        text, pressed = QInputDialog.getText(self, widget_name, widget_text, QLineEdit.Normal, "")
        if pressed and text != '':
            return text
        return None

    def handle_login(self):
        username = self.get_text("Login", "Email:")
        if not username:
            reply = QMessageBox.question(self, 'PyQt5 message', "Email empty! wanna retry?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        password = self.get_text("Login", "Password:")
        if not password:
            reply = QMessageBox.question(self, 'PyQt5 message', "Password empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        # TODO: send username and password to Django for Login

        self.show_main_menu()

    def handle_signup(self):
        username = self.get_text("Sign up", "Email:")
        if not username:
            reply = QMessageBox.question(self, 'PyQt5 message', "Email empty! wanna retry?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        password = self.get_text("Sign up", "Password:")
        if not password:
            reply = QMessageBox.question(self, 'PyQt5 message', "Password empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        # TODO: send username and password to Django for Signup

        self.show_main_menu()

    def show_main_menu(self):

        # new note button
        new_note = QPushButton("ایجاد یادداشت جدید")
        new_note.setSizePolicy(QSizePolicy.Preferred,
                               QSizePolicy.Preferred)
        new_note.setStyleSheet("background-color: rgb(228, 210, 86)")

        # new group button
        new_group = QPushButton("ایجاد دسته جدید")
        new_group.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Preferred)
        new_group.setStyleSheet("background-color: rgb(228, 210, 86)")

        # view group
        view_groups = QPushButton("مشاهده دسته های قبلی")
        view_groups.setSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.Preferred)
        view_groups.setStyleSheet("background-color: rgb(228, 210, 86)")

        exit_page = QPushButton("خروج")
        exit_page.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Preferred)
        exit_page.setStyleSheet("background-color: rgb(228, 210, 86)")

        # set layout
        self.clear_layout(self.layout)

        self.layout.setRowStretch(0, 10)
        self.layout.setRowStretch(1, 10)
        self.layout.setRowStretch(2, 10)
        self.layout.setRowStretch(3, 5)
        self.layout.addWidget(new_note, 0, 2)
        self.layout.addWidget(new_group, 1, 2)
        self.layout.addWidget(view_groups, 2, 2)
        self.layout.addWidget(exit_page, 3, 0)
        self.layout.setSpacing(100)

        new_note.clicked.connect(self.show_note_menu)
        new_group.clicked.connect(self.handle_add_section)
        view_groups.clicked.connect(self.show_sections_list)
        exit_page.clicked.connect(self.quit_app)

    def handle_add_section(self):
        section_name = self.get_text("New Section", "Section name:")
        if not section_name:
            reply = QMessageBox.question(self, 'PyQt5 message', "Section name empty! wanna retry?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_add_section()
            else:
                return

        self.notebook.add_section(Section(section_name))

        # TODO: settle information with django in some way

    def show_note_menu(self):
        # reminder button
        remind_note = QPushButton("یادآوری")
        remind_note.setSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.Preferred)
        remind_note.setStyleSheet("background-color: rgb(228, 210, 86)")

        # edit button
        edit_note = QPushButton("ویرایش")
        edit_note.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Preferred)
        edit_note.setStyleSheet("background-color: rgb(228, 210, 86)")

        # save button
        save_note = QPushButton("ثبت")
        save_note.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Preferred)
        save_note.setStyleSheet("background-color: rgb(228, 210, 86)")

        # delete button
        delete_note = QPushButton("حذف")
        delete_note.setSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.Preferred)
        delete_note.setStyleSheet("background-color: rgb(228, 210, 86)")
        
        layout_topbar = QHBoxLayout()
        layout_topbar.addWidget(remind_note)
        layout_topbar.addWidget(edit_note)
        layout_topbar.addWidget(save_note)
        layout_topbar.addWidget(delete_note)
        layout_topbar.setSpacing(50)
        
        wid = QWidget()
        wid.setLayout(layout_topbar)

        text_box = QPlainTextEdit(self)

        self.clear_layout(self.layout)

        self.layout.setRowStretch(0, 5)
        self.layout.setRowStretch(1, 20)
        self.layout.addWidget(wid, 0, 2)
        self.layout.addWidget(text_box, 1, 2)
        self.layout.setSpacing(100)

    def show_sections_list(self):
        # quit button
        exit_page = QPushButton("خروج")
        exit_page.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Preferred)
        exit_page.setStyleSheet("background-color: rgb(228, 210, 86)")

        # delete button
        delete_section = QPushButton("حذف")
        delete_section.setSizePolicy(QSizePolicy.Preferred,
                                     QSizePolicy.Preferred)
        delete_section.setStyleSheet("background-color: rgb(228, 210, 86)")

        buttons = []
        layout_topbar = QVBoxLayout()
        for s in self.notebook.sections:
            btn = QPushButton(s.name)
            btn.setSizePolicy(QSizePolicy.Preferred,
                              QSizePolicy.Preferred)
            btn.setStyleSheet("background-color: rgb(228, 210, 86)")
            layout_topbar.addWidget(btn)
            buttons.append(btn)
        layout_topbar.setSpacing(50)
        
        wid = QWidget()
        wid.setLayout(layout_topbar)

        self.clear_layout(self.layout)

        self.layout.setRowStretch(0, 20)
        self.layout.setRowStretch(1, 5)
        self.layout.addWidget(wid, 0, 2)
        self.layout.addWidget(exit_page, 1, 0)
        self.layout.addWidget(delete_section, 1, 3)
        self.layout.setSpacing(50)

        # check which button is hit
        for btn in buttons:
            btn.clicked.connect(self.show_notes_list)
        
    def show_notes_list(self, group):
        # groups most later be created and turn groups and notes into objects
        self.notes = ['خواب ها', 'رفتار ها', 'مضامین']
        
        # quit button
        savenote = QPushButton("ایجاد یادداشت جدید")
        savenote.setSizePolicy(QSizePolicy.Preferred,
                               QSizePolicy.Preferred)
        savenote.setStyleSheet("background-color: rgb(228, 210, 86)")

        # delete button
        delnote = QPushButton("حذف")
        delnote.setSizePolicy(QSizePolicy.Preferred,
                              QSizePolicy.Preferred)
        delnote.setStyleSheet("background-color: rgb(228, 210, 86)")
        
        layout_topbar = QVBoxLayout()
        for note in self.notes:
            btn = QPushButton(note)
            btn.setSizePolicy(QSizePolicy.Preferred,
                              QSizePolicy.Preferred)
            btn.setStyleSheet("background-color: rgb(228, 210, 86)")
            layout_topbar.addWidget(btn)
        layout_topbar.setSpacing(50)
        
        wid = QWidget()
        wid.setLayout(layout_topbar)

        self.clear_layout(self.layout)

        self.layout.setRowStretch(0, 20)
        self.layout.setRowStretch(1, 5)
        self.layout.addWidget(wid, 0, 2)
        self.layout.addWidget(savenote, 1, 0)
        self.layout.addWidget(delnote, 1, 3)
        self.layout.setSpacing(50)
        
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
