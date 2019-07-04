'''
Created on May 23, 2019

@author: amin
'''

from PyQt5.QtWidgets import (QPushButton, QPlainTextEdit, QVBoxLayout,
                             QHBoxLayout, QWidget, QGridLayout, QInputDialog,
                             QLineEdit, QMessageBox, QSizePolicy)
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor
from Notebook import Notebook
from Note import Note
from Section import Section
from Network import Network
import time
import datetime

class MainWidget(QWidget):
    def __init__(self):
        self.layout = None
        self.notebook = None
        self.network = Network()
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

    def handle_login(self, create_new=False):
        username = self.get_text("Login", "Email:")
        if not username:
            reply = QMessageBox.question(self, 'Message', "Email empty! wanna retry?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        password = self.get_text("Login", "Password:")
        if not password:
            reply = QMessageBox.question(self, 'Message', "Password empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        ret = self.network.login_user(username, password)
        QMessageBox.about(self, 'Message', ret[1])
        if not ret[0]:
            return

        # login means that this user has already a notebook in server
        if create_new:
            self.network.create_notebook(self.notebook)
        else:
            print('HERE')
            self.notebook = self.network.download_notebook(username=username)
        self.show_main_menu()

    def handle_signup(self):
        username = self.get_text("Sign up", "Email:")
        if not username:
            reply = QMessageBox.question(self, 'Message', "Email empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        password = self.get_text("Sign up", "Password:")
        if not password:
            reply = QMessageBox.question(self, 'Message', "Password empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_login()
            else:
                return

        ret = self.network.signup_user(username, password)
        QMessageBox.about(self, 'Message', ret[1] + ' Please login!')
        if not ret[0]:
            return

        # successful signup means we should create a notebook for him
        self.notebook = Notebook(username=username)
        self.handle_login(create_new=True)

    def show_main_menu(self):
        print('show_main_menu', self.notebook.username)
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

        new_note.clicked.connect(lambda: self.show_note_menu(None, None))
        new_group.clicked.connect(self.handle_add_section)
        view_groups.clicked.connect(self.show_sections_list)
        exit_page.clicked.connect(self.quit_app)

    def handle_add_section(self):
        print('handle_add_section', self.notebook.username)
        section_name = self.get_text("New Section", "Section name:")
        if not section_name:
            reply = QMessageBox.question(self, 'Message', "Section name empty! wanna retry?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_add_section()
            else:
                return

        self.notebook.add_section(Section(section_name))
        self.network.update_notebook(self.notebook)

    def get_note_and_section_name(self, section_name):
        note_name = self.get_text("New Note", "Pick a name:")
        if not note_name:
            reply = QMessageBox.question(self, 'Message', "Name empty! wanna retry?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.get_note_and_section_name()
            else:
                return

        if section_name is None:
            section_name = self.get_text("Section", "Which section?")
            if not note_name:
                reply = QMessageBox.question(self, 'Message', "Section empty! wanna retry?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.get_note_and_section_name()
                else:
                    return

        section = None
        for s in self.notebook.sections:
            if s.name == section_name:
                section = s

        if section is None:
            section = Section(section_name)
            self.notebook.add_section(section)

        note = Note(note_name, "")
        section.add_note(note)
        return note, section_name

    def show_note_menu(self, note, section_name, is_editable=False):
        if note is None and section_name is None:
            note, section_name = self.get_note_and_section_name(None)
        elif note is None:
            note, section_name = self.get_note_and_section_name(section_name)

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
        text_box.setEnabled(is_editable)

        if isinstance(note, Note):
            text_box.setPlainText(note.data)

        self.clear_layout(self.layout)

        self.layout.setRowStretch(0, 5)
        self.layout.setRowStretch(1, 20)
        self.layout.addWidget(wid, 0, 2)
        self.layout.addWidget(text_box, 1, 2)
        self.layout.setSpacing(100)

        remind_note.clicked.connect(lambda: self.set_note_reminder(note))
        save_note.clicked.connect(lambda: self.handle_save_note(note, section_name, text_box.toPlainText()))
        delete_note.clicked.connect(lambda: self.handle_delete_note(section_name, note.name))
        edit_note.clicked.connect(lambda: self.set_editable(note, section_name))

    def set_editable(self, note, section_name):
        self.show_note_menu(note, section_name, True)

    def handle_save_note(self, note, section_name, data):
        note.data = data
        self.show_notes_list(section_name)
        self.network.update_notebook(self.notebook)

    def set_note_reminder(self, note):
        date = self.get_text("Reminder", "Enter time(yyyy mm dd hh mm ss):")
        if not date:
            reply = QMessageBox.question(self, 'Message', "empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.set_note_reminder()
            else:
                return

        year, month, day, hour, minute, second = date.split()

        dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        ret = self.network.set_timer(self.notebook.username, note.name, time.mktime(dt.timetuple()))
        QMessageBox.about(self, 'Reminder', ret[1])

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

        layout_topbar = QVBoxLayout()
        for s in self.notebook.sections:
            btn = QPushButton(s.name)
            btn.setSizePolicy(QSizePolicy.Preferred,
                              QSizePolicy.Preferred)
            btn.setStyleSheet("background-color: rgb(228, 210, 86)")
            layout_topbar.addWidget(btn)
            btn.clicked.connect(lambda: self.show_notes_list(s.name))
            print(s.name)
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

        # set action for each button
        delete_section.clicked.connect(self.handle_delete_section)
        exit_page.clicked.connect(self.show_main_menu)

    def handle_delete_section(self):
        section_name = self.get_text("Delete Section", "Section name:")
        if not section_name:
            reply = QMessageBox.question(self, 'Message', "Section name empty! wanna retry?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.handle_delete_section()
            else:
                return

        self.notebook.remove_section(section_name)
        self.network.update_notebook(self.notebook)
        self.show_sections_list()

    def show_notes_list(self, section_name):
        print(section_name)
        # section name
        section_label = QPushButton(section_name)
        section_label.setSizePolicy(QSizePolicy.Preferred,
                                    QSizePolicy.Preferred)
        section_label.setStyleSheet("background-color: rgb(228, 210, 86)")

        # quit button
        new_note = QPushButton("ایجاد یادداشت جدید")
        new_note.setSizePolicy(QSizePolicy.Preferred,
                               QSizePolicy.Preferred)
        new_note.setStyleSheet("background-color: rgb(228, 210, 86)")

        # delete button
        exit_button = QPushButton("خروج")
        exit_button.setSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.Preferred)
        exit_button.setStyleSheet("background-color: rgb(228, 210, 86)")

        for s in self.notebook.sections:
            if s.name == section_name:
                section = s
                break

        buttons = []
        layout_topbar = QVBoxLayout()
        for note in section.notes:
            btn = QPushButton(note.name)
            btn.setSizePolicy(QSizePolicy.Preferred,
                              QSizePolicy.Preferred)
            btn.setStyleSheet("background-color: rgb(228, 210, 86)")
            layout_topbar.addWidget(btn)
            buttons.append((btn, note))
        layout_topbar.setSpacing(50)
        
        wid = QWidget()
        wid.setLayout(layout_topbar)

        self.clear_layout(self.layout)

        self.layout.setRowStretch(0, 2)
        self.layout.setRowStretch(1, 5)
        self.layout.setRowStretch(2, 3)
        self.layout.addWidget(wid, 1, 2)
        self.layout.addWidget(new_note, 2, 0)
        self.layout.addWidget(exit_button, 2, 3)
        self.layout.addWidget(section_label, 0, 2)
        self.layout.setSpacing(50)

        # set action for each node
        for (btn, note) in buttons:
            btn.clicked.connect(lambda: self.show_note_menu(note, section_name))
        new_note.clicked.connect(lambda: self.show_note_menu(None, section_name))
        exit_button.clicked.connect(self.show_sections_list)

    def handle_delete_note(self, section_name, note_name):
        print('handle_delete_note', self.notebook.username)
        if note_name is None:
            note_name = self.get_text("Delete Note", "Note name:")
            if not note_name:
                reply = QMessageBox.question(self, 'Message', "Section name empty! wanna retry?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.handle_delete_note(section_name, note_name)
                else:
                    return

        for s in self.notebook.sections:
            if s.name == section_name:
                s.del_note(note_name)
                break

        self.network.update_notebook(self.notebook)
        self.show_notes_list(section_name)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

