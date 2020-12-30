import json
import os
import re
import sys
from socket import socket, AF_INET, SOCK_STREAM

import PySide6
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QIntValidator
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem, QTableWidgetItem, QPushButton, \
    QLineEdit, QLabel, QSizePolicy, QFileDialog

from AddBookmarkDialog import Ui_Dialog as AddBookmarkForm
from ChapterView import Ui_Form as ChapterForm
from ContentView import Ui_Form as ContentForm
from LoginView import Ui_Form as LoginForm
from MainWindow import Ui_MainWindow
from RegisterView import Ui_Form as RegForm
from UserBookmarkView import Ui_Form as UserBookmarkForm
from WelcomeView import Ui_Form as WelcomeForm


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.view = None
        self.uid = None
        self.b_id = None
        self.chap_id = None
        self.page_num = None
        self.page_length = None
        self.label_choose_page = None
        self.widget_choose_page = None
        self.add_bookmark_dialog = None
        self.add_signal_func = {
            LoginView: self.add_LoginView_signal,
            RegisterView: self.add_RegisterView_signal,
            WelcomeView: self.add_WelcomeView_signal,
            UserBookmarkView: self.add_UserBookmarkView_signal,
            ChapterView: self.add_ChapterView_signal,
            ContentView: self.add_ContentView_signal,
            BookBookmarkView: self.add_BookBookmarkView_signal
        }
        self.remove_signal_func = {
            LoginView: self.remove_LoginView_signal,
            RegisterView: self.remove_RegisterView_signal,
            WelcomeView: self.remove_WelcomeView_signal,
            UserBookmarkView: self.remove_BookmarkView_signal,
            ChapterView: self.remove_ChapterView_signal,
            ContentView: self.remove_ContentView_signal,
            BookBookmarkView: self.remove_BookmarkView_signal
        }
        self.add_view(LoginView, None)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        if self.uid is not None:
            get_logout_response(self.uid)
        event.accept()

    def display_status_message(self, message, timeout=0):
        self.MainStatusBar.showMessage(message, timeout)

    def toggle_view(self, subview):
        old_view = type(self.view)
        self.remove_view()
        self.add_view(subview, old_view)

    def add_view(self, subview, old_view):
        assert subview in {LoginView, RegisterView, WelcomeView, UserBookmarkView, ChapterView, ContentView,
                           BookBookmarkView}
        if subview == UserBookmarkView:
            self.view = subview(self.uid)
        elif subview == ChapterView:
            self.view = subview(self.b_id)
        elif subview == ContentView:
            self.view = subview(self.b_id, self.chap_id, self.page_num)
            self.page_num, self.page_length = self.view.get_page_info()
        elif subview == BookBookmarkView:
            self.view = subview(self.uid, self.b_id)
        else:
            self.view = subview()
        self.MainGridLayout.addWidget(self.view)
        self.add_signal_func.get(subview, lambda x: None)(old_view)
        self.view.show()

    def remove_view(self):
        type_of_view = type(self.view)
        assert type_of_view in {LoginView, RegisterView, WelcomeView, UserBookmarkView, ChapterView, ContentView,
                                BookBookmarkView}
        self.view.hide()
        self.remove_signal_func.get(type_of_view, lambda: None)()

        self.MainToolBar.clear()
        self.MainGridLayout.removeWidget(self.view)
        self.view = None

    def add_LoginView_signal(self, old_view):
        self.view.login_button_signal.connect(self.toggle_view)
        self.view.register_button_signal.connect(self.toggle_view)
        self.view.display_status_signal.connect(self.display_status_message)
        self.view.set_current_user_signal.connect(self.set_current_user)

    def remove_LoginView_signal(self):
        self.view.login_button_signal.disconnect(self.toggle_view)
        self.view.register_button_signal.disconnect(self.toggle_view)
        self.view.display_status_signal.disconnect(self.display_status_message)
        self.view.set_current_user_signal.disconnect(self.set_current_user)

    def add_RegisterView_signal(self, old_view):
        self.view.submit_button_signal.connect(self.toggle_view)
        self.view.display_status_signal.connect(self.display_status_message)

    def remove_RegisterView_signal(self):
        self.view.submit_button_signal.disconnect(self.toggle_view)
        self.view.display_status_signal.disconnect(self.display_status_message)

    def add_WelcomeView_signal(self, old_view):
        self.view.select_book_signal.connect(self.toggle_view)
        self.view.display_status_signal.connect(self.display_status_message)
        self.view.set_current_book_signal.connect(self.set_current_book)

        action_logout = QAction('Logout', self)
        action_explore_bookmark = QAction('My Bookmark', self)
        action_logout.triggered.connect(self.logout_action_onclick)
        action_explore_bookmark.triggered.connect(lambda: self.toggle_view(UserBookmarkView))
        self.MainToolBar.addAction(action_logout)
        self.MainToolBar.addAction(action_explore_bookmark)

    def remove_WelcomeView_signal(self):
        self.view.select_book_signal.disconnect(self.toggle_view)
        self.view.display_status_signal.disconnect(self.display_status_message)
        self.view.set_current_book_signal.disconnect(self.set_current_book)

    def add_BookmarkView_signal(self):
        self.view.display_status_signal.connect(self.display_status_message)
        self.view.set_current_book_signal.connect(self.set_current_book)
        self.view.set_current_chapter_signal.connect(self.set_current_chapter)
        self.view.set_current_page_signal.connect(self.set_current_page)
        self.view.select_chapter_signal.connect(self.toggle_view)

    def remove_BookmarkView_signal(self):
        self.view.display_status_signal.disconnect(self.display_status_message)
        self.view.set_current_book_signal.disconnect(self.set_current_book)
        self.view.set_current_chapter_signal.disconnect(self.set_current_chapter)
        self.view.set_current_page_signal.disconnect(self.set_current_page)
        self.view.select_chapter_signal.disconnect(self.toggle_view)

    def add_UserBookmarkView_signal(self, old_view):
        self.add_BookmarkView_signal()
        action_back = QAction('Back', self)
        action_remove_all = QAction('Remove all', self)
        action_back.triggered.connect(lambda: self.toggle_view(old_view))
        action_remove_all.triggered.connect(lambda: self.view.delete_bookmark_all('user'))
        self.MainToolBar.addAction(action_back)
        self.MainToolBar.addAction(action_remove_all)

    def add_ChapterView_signal(self, old_view):
        self.view.display_status_signal.connect(self.display_status_message)
        self.view.select_chapter_signal.connect(self.toggle_view)
        self.view.set_current_chapter_signal.connect(self.set_current_chapter)

        action_back = QAction('Back', self)
        action_explore_bookmark = QAction('My Bookmark', self)
        action_back.triggered.connect(lambda: self.toggle_view(WelcomeView))
        action_explore_bookmark.triggered.connect(lambda: self.toggle_view(BookBookmarkView))
        self.MainToolBar.addAction(action_back)
        self.MainToolBar.addAction(action_explore_bookmark)

    def remove_ChapterView_signal(self):
        self.view.display_status_signal.disconnect(self.display_status_message)
        self.view.select_chapter_signal.disconnect(self.toggle_view)
        self.view.set_current_chapter_signal.disconnect(self.set_current_chapter)

    def add_ContentView_signal(self, old_view):
        self.view.set_current_page_signal.connect(self.set_current_page)
        self.view.set_page_length_signal.connect(self.set_page_length)
        action_back = QAction('Back', self)
        action_chapter_minus = QAction('<<', self)
        action_page_minus = QAction('<', self)
        action_page_plus = QAction('>', self)
        action_chapter_plus = QAction('>>', self)
        action_add_bookmark = QAction('Add Bookmark', self)
        action_explore_bookmark = QAction('My Bookmark', self)
        action_download = QAction('Download', self)
        self.label_choose_page = QLabel(f' ( {self.page_num + 1} / {self.page_length} ) ')

        self.widget_choose_page = QLineEdit()
        self.widget_choose_page.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.widget_choose_page.setFixedWidth(60)
        self.widget_choose_page.setAlignment(Qt.AlignCenter)
        self.widget_choose_page.setValidator(QIntValidator(self.page_num + 1, self.page_length))

        action_chapter_minus.setToolTip('Chapter Up')
        action_page_minus.setToolTip('Page Up')
        action_page_plus.setToolTip('Page Down')
        action_chapter_plus.setToolTip('Chapter Up')

        action_back.triggered.connect(lambda: self.toggle_view(ChapterView))
        action_chapter_minus.triggered.connect(self.chapter_minus_onclick)
        action_page_minus.triggered.connect(self.page_minus_onclick)
        action_page_plus.triggered.connect(self.page_plus_onclick)
        action_chapter_plus.triggered.connect(self.chapter_plus_onclick)
        action_add_bookmark.triggered.connect(self.open_add_bookmark_dialog)
        action_explore_bookmark.triggered.connect(lambda: self.toggle_view(BookBookmarkView))
        action_download.triggered.connect(self.download_file)
        self.widget_choose_page.editingFinished.connect(self.page_choose_onfinish)

        self.MainToolBar.addAction(action_back)
        self.MainToolBar.addSeparator()
        self.MainToolBar.addActions([action_chapter_minus, action_page_minus])
        self.MainToolBar.addWidget(self.widget_choose_page)
        self.MainToolBar.addWidget(self.label_choose_page)
        self.MainToolBar.addActions([action_page_plus, action_chapter_plus])
        self.MainToolBar.addSeparator()
        self.MainToolBar.addActions([action_add_bookmark, action_explore_bookmark, action_download])

    def remove_ContentView_signal(self):
        self.view.set_current_page_signal.disconnect(self.set_current_page)
        self.view.set_page_length_signal.disconnect(self.set_page_length)

    def add_BookBookmarkView_signal(self, old_view):
        self.add_BookmarkView_signal()
        action_back = QAction('Back', self)
        action_remove_all = QAction('Remove all', self)
        action_back.triggered.connect(lambda: self.toggle_view(old_view))
        action_remove_all.triggered.connect(lambda: self.view.delete_bookmark_all('user_book', self.view.b_id))
        self.MainToolBar.addAction(action_back)
        self.MainToolBar.addAction(action_remove_all)

    def download_file(self):
        file_path = QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', 'Texts (*.txt)')[0]
        file_content = get_chapter('single', self.b_id, self.chap_id)[1]
        if file_content == []:
            self.display_status_message('Fail to download.', 2000)
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(file_content)
        self.display_status_message('Successfully downloaded.', 2000)

    def set_current_user(self, uid):
        self.uid = uid

    def set_current_book(self, b_id):
        self.b_id = b_id

    def set_current_chapter(self, chap_id):
        self.chap_id = chap_id

    def set_page_length(self, page_length):
        self.page_length = page_length
        if self.label_choose_page is not None:
            self.label_choose_page.setText(f' ( {self.page_num + 1} / {self.page_length} ) ')

    def set_current_page(self, page_num):
        self.page_num = page_num
        if self.label_choose_page is not None:
            self.label_choose_page.setText(f' ( {self.page_num + 1} / {self.page_length} ) ')

    def page_minus_onclick(self):
        if self.page_num == 0:
            self.display_status_message('We are at the first page.', 2000)
        else:
            self.set_current_page(self.page_num - 1)
            self.view.set_page(self.page_num)

    def page_plus_onclick(self):
        if self.page_num == self.page_length - 1:
            self.display_status_message('We are at the last page.', 2000)
        else:
            self.set_current_page(self.page_num + 1)
            self.view.set_page(self.page_num)

    def page_choose_onfinish(self):
        page_num = int(self.widget_choose_page.text()) - 1
        self.set_current_page(page_num)
        self.view.set_page(page_num)

    def chapter_minus_onclick(self):
        chap_list = get_chapter('simple', self.b_id)
        chap_list.sort()
        pos = chap_list.index(self.chap_id)
        if pos == 0:
            self.display_status_message('We are at the first chapter.', 2000)
        else:
            self.chap_id = chap_list[pos - 1]
            self.view.refresh(self.b_id, self.chap_id)

    def chapter_plus_onclick(self):
        chap_list = get_chapter('simple', self.b_id)
        chap_list.sort()
        chap_list_length = len(chap_list)
        pos = chap_list.index(self.chap_id)
        if pos == chap_list_length - 1:
            self.display_status_message('We are at the last chapter.', 2000)
        else:
            self.chap_id = chap_list[pos + 1]
            self.view.refresh(self.b_id, self.chap_id)

    def open_add_bookmark_dialog(self):
        self.add_bookmark_dialog = AddBookmarkDialog()

        self.add_bookmark_dialog.display_status_signal.connect(self.display_status_message)
        self.add_bookmark_dialog.close_dialog_signal.connect(self.close_add_bookmark_dialog)
        self.add_bookmark_dialog.transmit_bookmark_name_signal.connect(self.add_bookmark)

        self.add_bookmark_dialog.show()

    def close_add_bookmark_dialog(self):
        self.add_bookmark_dialog.close()

        self.add_bookmark_dialog.display_status_signal.disconnect(self.display_status_message)
        self.add_bookmark_dialog.close_dialog_signal.disconnect(self.close_add_bookmark_dialog)
        self.add_bookmark_dialog.transmit_bookmark_name_signal.disconnect(self.add_bookmark)

        self.add_bookmark_dialog = None

    def add_bookmark(self, bm_name):
        request = {
            'type': 'get_bookmark_id',
            'data': {}
        }
        resp = get_response(request)
        assert resp['type'] == 'get_bookmark_id'
        resp_data = resp['data']
        if resp_data['status'] == 'error':
            return resp['type']
        bm_id = resp_data['content']
        return add_bookmark(self.uid, self.b_id, bm_id, bm_name, self.chap_id, self.page_num)

    def logout_action_onclick(self):
        resp = get_logout_response(self.uid)
        assert resp['type'] == 'logout'
        resp_data = resp['data']
        self.uid = None
        self.toggle_view(LoginView)
        message = 'Successfully Logouted.' if resp_data['status'] == 'ok' else resp_data['type']
        self.display_status_message(message, 3000)


class LoginView(QWidget, LoginForm):
    login_button_signal = Signal(type)
    register_button_signal = Signal(type)
    display_status_signal = Signal(str, int)
    set_current_user_signal = Signal(str)

    def __init__(self):
        super(LoginView, self).__init__()
        self.setupUi(self)

        self.uid_empty = True
        self.psw_empty = True
        self.UidInput.textChanged.connect(lambda: self.button_enable_checker('uid'))
        self.PswInput.textChanged.connect(lambda: self.button_enable_checker('psw'))

        self.RegBtn.clicked.connect(lambda: self.register_button_signal.emit(RegisterView))
        self.LoginBtn.clicked.connect(self.login_button_onclick)

    def login_button_onclick(self):
        uid, psw = self.UidInput.text(), self.PswInput.text()
        data = {
            'type': 'login',
            'data': {
                'uid': uid,
                'psw': psw
            }
        }
        resp = get_response(data)
        assert resp['type'] == 'login'
        resp_data = resp['data']
        if resp_data['status'] == 'ok':
            self.display_status_signal.emit('Successfully logined.', 3000)
            self.set_current_user_signal.emit(uid)
            self.login_button_signal.emit(WelcomeView)
        else:
            self.UidInput.clear()
            self.PswInput.clear()
            self.display_status_signal.emit(resp_data['type'], 5000)

    def button_enable_checker(self, val):
        assert val in {'uid', 'psw'}
        if val == 'uid':
            self.uid_empty = (self.UidInput.text() == '')
        else:
            self.psw_empty = (self.PswInput.text() == '')
        self.LoginBtn.setEnabled(self.uid_empty is False and self.psw_empty is False)


class RegisterView(QWidget, RegForm):
    submit_button_signal = Signal(type)
    display_status_signal = Signal(str, int)

    def __init__(self):
        super(RegisterView, self).__init__()
        self.setupUi(self)

        self.uid_empty = True
        self.psw_empty = True
        self.rep_psw_empty = True

        self.UidInput.textChanged.connect(lambda: self.button_enable_checker('uid'))
        self.PswInput.textChanged.connect(lambda: self.button_enable_checker('psw'))
        self.RepPswInput.textChanged.connect(lambda: self.button_enable_checker('rep_psw'))

        self.RegSubmitBtn.clicked.connect(self.submit_button_onclick)

    def button_enable_checker(self, val):
        assert val in {'uid', 'psw', 'rep_psw'}
        if val == 'uid':
            self.uid_empty = (self.UidInput.text() == '')
        elif val == 'psw':
            self.psw_empty = (self.PswInput.text() == '')
        else:
            self.rep_psw_empty = (self.RepPswInput.text() == '')

        flag = self.PswInput.text() == self.RepPswInput.text()
        self.RepPswChecker.setChecked(flag)
        self.RegSubmitBtn.setEnabled((self.uid_empty or self.psw_empty or self.rep_psw_empty) is False and flag)

    def submit_button_onclick(self):
        uid = self.UidInput.text()
        psw = self.PswInput.text()
        email = self.EmailInput.text()
        data = {
            'type': 'register',
            'data': {
                'uid': uid,
                'psw': psw,
                'email': email
            }
        }
        resp = get_response(data)
        assert resp['type'] == 'register'
        resp_data = resp['data']
        if resp_data['status'] == 'ok':
            self.display_status_signal.emit('Successfully registered.', 3000)
            self.submit_button_signal.emit(LoginView)
        else:
            self.UidInput.clear()
            self.PswInput.clear()
            self.EmailInput.clear()
            self.RepPswInput.clear()
            self.display_status_signal.emit(resp_data['type'], 5000)


class WelcomeView(QWidget, WelcomeForm):
    select_book_signal = Signal(type)
    display_status_signal = Signal(str, int)
    set_current_book_signal = Signal(int)

    def __init__(self):
        super(WelcomeView, self).__init__()
        self.setupUi(self)

        self.has_clicked = False

        book_list = get_book('all')
        for book in book_list:
            book_item = BookListItem(book['book_id'], book['name'])
            self.BookListWidget.addItem(book_item)

        self.BookListWidget.itemClicked.connect(self.item_onclick)
        self.BookListWidget.itemDoubleClicked.connect(self.item_onclick_double)

    def item_onclick_double(self, item):
        self.set_current_book_signal.emit(item.b_id)
        self.select_book_signal.emit(ChapterView)

    def item_onclick(self, item):
        synopsis_text = self.SynopsisTextEdit.toPlainText()
        if not self.has_clicked:
            self.has_clicked = True
        else:
            index = synopsis_text.find('\n\n')
            synopsis_text = synopsis_text[index + 2:]
        self.SynopsisTextEdit.setPlainText(item.text() + '\n\n' + synopsis_text)


class BookListItem(QListWidgetItem):
    def __init__(self, b_id, name):
        super(BookListItem, self).__init__(name)
        self.b_id = b_id


class ChapterItem(QListWidgetItem):
    def __init__(self, chap_id):
        super(ChapterItem, self).__init__(f'Chapter {chap_id}')
        self.chap_id = chap_id


class BookTableItem(QTableWidgetItem):
    def __init__(self, b_id, name):
        super(BookTableItem, self).__init__(name)
        self.b_id = b_id


class BookmarkView(QWidget, UserBookmarkForm):
    display_status_signal = Signal(str, int)
    set_current_book_signal = Signal(int)
    set_current_chapter_signal = Signal(int)
    set_current_page_signal = Signal(int)
    select_chapter_signal = Signal(type)

    def __init__(self, uid):
        super(BookmarkView, self).__init__()
        self.setupUi(self)

        self.uid = uid

        self.tableWidget.itemDoubleClicked.connect(self.item_onclick_double)

    def item_onclick_double(self, item):
        current_row = self.tableWidget.row(item)
        b_id = self.tableWidget.item(current_row, 2).b_id
        chap_id = int(self.tableWidget.item(current_row, 3).text())
        page_num = int(self.tableWidget.item(current_row, 4).text())

        self.set_current_book_signal.emit(b_id)
        self.set_current_chapter_signal.emit(chap_id)
        self.set_current_page_signal.emit(page_num)
        self.select_chapter_signal.emit(ContentView)

    def delete_bookmark_single(self):
        row_num = self.tableWidget.currentRow()
        bm_id = int(self.tableWidget.item(row_num, 0).text())
        self.tableWidget.removeRow(row_num)
        self.tableWidget.resizeColumnsToContents()
        message = delete_bookmark_single(bm_id)
        self.display_status_signal.emit(message, 3000)

    def delete_bookmark_all(self, request_type):
        self.tableWidget.clearContents()
        self.tableWidget.resizeColumnsToContents()
        message = delete_bookmark_user(request_type, self.uid)
        self.display_status_signal.emit(message, 3000)

    def get_user_bookmark(self, request_type, b_id=None):
        bookmark_list = get_bookmark_list(request_type, self.uid, b_id)
        bookmark_list_length = len(bookmark_list)
        table_header = ['bookmark_id', 'name', 'book_id', 'chapter_id', 'page_num']
        table_header_length = len(table_header)
        self.tableWidget.setRowCount(bookmark_list_length)
        for i in range(bookmark_list_length):
            bookmark = bookmark_list[i]
            if request_type == 'user':
                b_id = bookmark['book_id']
            else:
                assert b_id is not None
            for j in range(table_header_length):
                is_book_id = table_header[j] == 'book_id'
                if is_book_id:
                    text = get_book('single', b_id)['name']
                else:
                    text = bookmark[table_header[j]]
                if type(text) == int: text = str(text)
                if is_book_id:
                    new_item = BookTableItem(b_id, text)
                else:
                    new_item = QTableWidgetItem(text)
                new_item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, new_item)
            remove_button = QPushButton('delete')
            remove_button.clicked.connect(self.delete_bookmark_single)
            self.tableWidget.setCellWidget(i, table_header_length, remove_button)
        self.tableWidget.resizeColumnsToContents()


class UserBookmarkView(BookmarkView):
    def __init__(self, uid):
        super(UserBookmarkView, self).__init__(uid)

        self.get_user_bookmark('user')


class BookBookmarkView(BookmarkView):
    def __init__(self, uid, b_id):
        super(BookBookmarkView, self).__init__(uid)

        self.b_id = b_id
        self.get_user_bookmark('user_book', self.b_id)


class ChapterView(QWidget, ChapterForm):
    display_status_signal = Signal(str, int)
    select_chapter_signal = Signal(type)
    set_current_chapter_signal = Signal(int)

    def __init__(self, b_id):
        super(ChapterView, self).__init__()
        self.setupUi(self)

        self.b_id = b_id

        b_name = get_book('single', b_id)['name']
        self.BookLabel.setText(f'## {b_name}')

        chapter_list = get_chapter('simple', self.b_id)
        for chapter in chapter_list:
            chapter_item = ChapterItem(chapter)
            self.ChapterListWidget.addItem(chapter_item)

        self.ChapterListWidget.itemClicked.connect(self.item_onclick)
        self.ChapterListWidget.itemDoubleClicked.connect(self.item_onclick_double)

    def item_onclick(self, item):
        chap_content = get_chapter('single', self.b_id, item.chap_id)[1]
        i, cnt, n, flag = 0, 0, len(chap_content), False
        for i in range(n):
            if chap_content[i] == '\n': cnt += 1
            if cnt == 8:
                flag = True
                break
        text = chap_content[:i + 1]
        if flag: text += '\n......'
        self.SynopsisTextEdit.setPlainText(text)

    def item_onclick_double(self, item):
        self.set_current_chapter_signal.emit(item.chap_id)
        self.select_chapter_signal.emit(ContentView)


class ContentView(QWidget, ContentForm):
    set_current_page_signal = Signal(int)
    set_page_length_signal = Signal(int)

    def __init__(self, b_id, chap_id, page_num):
        super(ContentView, self).__init__()
        self.setupUi(self)

        self.b_id, self.chap_id = None, None
        self.page_list, self.page_len, self.page_num = None, None, None

        self.refresh(b_id, chap_id, page_num)

    def refresh(self, b_id, chap_id, page_num=None):
        self.b_id = b_id
        self.chap_id = chap_id
        self.page_num = page_num
        self.page_list = get_pages(b_id, chap_id)
        self.page_len = len(self.page_list)
        if self.page_num is None:
            self.page_num = 0
        self.set_page_length_signal.emit(self.page_len)
        self.set_current_page_signal.emit(self.page_num)

        b_name = get_book('single', b_id)['name']
        self.ChapterLabel.setText(f'## {b_name} -- Chapter {chap_id}')
        self.ContentTextEdit.setPlainText(self.page_list[self.page_num])

    def get_page_info(self):
        return self.page_num, self.page_len

    def set_page(self, page_num):
        self.page_num = page_num
        self.ContentTextEdit.setPlainText(self.page_list[self.page_num])


class AddBookmarkDialog(QWidget, AddBookmarkForm):
    display_status_signal = Signal(str, int)
    close_dialog_signal = Signal()
    transmit_bookmark_name_signal = Signal(str)

    def __init__(self):
        super(AddBookmarkDialog, self).__init__()
        self.setupUi(self)

        self.buttonBox.buttons()[0].setEnabled(False)
        self.BookmarkNameEdit.textChanged.connect(self.button_enable_checker)

    def accept(self):
        self.transmit_bookmark_name_signal.emit(self.BookmarkNameEdit.text())
        self.close_dialog_signal.emit()

    def reject(self):
        self.close_dialog_signal.emit()

    def button_enable_checker(self):
        self.buttonBox.buttons()[0].setEnabled(self.BookmarkNameEdit.text() != '')


def get_pages(b_id, chap_id):
    content = get_chapter('single', b_id, chap_id)[1]
    content_length = len(content)
    x, y = 0, 0
    pages = []
    lines, line = [], ''
    for i in range(content_length):
        if content[i] == '\n':
            lines.append(line)
            line = ''
            x, y = x + 1, 0
        else:
            line += content[i]
            y += 1
        if y == 50:
            x, y = x + 1, 0
        if x == 19:
            lines.append(line)
            pages.append('\n'.join(lines))
            lines, line = [], ''
            x, y = 0, 0
    if line != '': lines.append(line)
    if lines: pages.append('\n'.join(lines))
    return pages


def add_bookmark(uid, b_id, bm_id, name, chap_id, page_num):
    request = {
        'type': 'add_bookmark',
        'data': {
            'uid': uid,
            'book_id': b_id,
            'bookmark_id': bm_id,
            'name': name,
            'chapter_id': chap_id,
            'page_num': page_num
        }
    }
    resp = get_response(request)
    assert resp['type'] == 'add_bookmark'
    resp_data = resp['data']
    if resp_data['status'] == 'ok':
        return 'Successfully added.'
    else:
        return resp_data['type']


def delete_bookmark_single(bm_id):
    request = {
        'type': 'del_bookmark_single',
        'data': {
            'bookmark_id': bm_id
        }
    }
    resp = get_response(request)
    assert resp['type'] == 'del_bookmark_single'
    resp_data = resp['data']
    if resp_data['status'] == 'ok':
        return 'Successfully deleted.'
    else:
        return resp_data['type']


def delete_bookmark_user(request_type, uid, b_id=None):
    resp_data = get_delete_bookmark_user('del_bookmark', request_type, uid, b_id)
    if resp_data['status'] == 'ok':
        return 'Successfully deleted.'
    else:
        return resp_data['type']


def get_bookmark_list(request_type, uid, b_id=None):
    resp_data = get_delete_bookmark_user('get_bookmark', request_type, uid, b_id)
    return resp_data['content']


def get_delete_bookmark_user(op_type, request_type, uid, b_id=None):
    assert op_type in {'get_bookmark', 'del_bookmark'}
    assert request_type in {'user', 'user_book'}
    request = {
        'type': op_type + '_' + request_type,
        'data': {'uid': uid}
    }
    if request_type == 'user_book':
        assert b_id is not None
        request['data']['book_id'] = b_id
    resp = get_response(request)
    assert resp['type'] == op_type + '_' + request_type
    return resp['data']


def get_book(request_type, b_id=None):
    assert request_type in {'single', 'all'}
    request = {
        'type': 'get_book_' + request_type,
        'data': {}
    }
    if request_type == 'single':
        assert b_id is not None
        request['data']['book_id'] = b_id
    resp = get_response(request)
    assert resp['type'] == 'get_book_' + request_type
    resp_data = resp['data']
    return resp_data['content']


def get_chapter(request_type, b_id, chap_id=None):
    assert request_type in {'single', 'all', 'simple'}
    request = {
        'type': 'get_chapter_' + request_type,
        'data': {'book_id': b_id}
    }
    if request_type == 'single':
        assert chap_id is not None
        request['data']['chapter_id'] = chap_id
    resp = get_response(request)
    assert resp['type'] == 'get_chapter_' + request_type
    resp_data = resp['data']
    return resp_data['content']


def get_logout_response(uid):
    data = {
        'type': 'logout',
        'data': {
            'uid': uid
        }
    }
    return get_response(data)


def init():
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


def get_response(request_dict: dict) -> dict:
    request_str = json.dumps(request_dict, ensure_ascii=False).encode(encoding='utf-8')
    return socket_send(request_str)


def socket_send(query: bytes) -> dict:
    # server_name, server_port = '127.0.0.1', 6370
    # server_name, server_port = '45.134.171.215', 6370
    server_name, server_port = sys.argv[1], int(sys.argv[2])
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    client_socket.send(query)
    tmp = client_socket.recv(1024 * 1024)
    recv_data = tmp.decode(encoding='utf-8')
    client_socket.close()
    reply = json.loads(recv_data)
    return reply


def ip_checker(addr):
    ip_compiler = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|'
                             '2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    return ip_compiler.match(addr)


def port_checker(port):
    try:
        port_int = int(port)
    except:
        return False
    if port_int >= 0 and port_int <= 65535:
        return True
    else:
        return False


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Argument length is too short.')
        sys.exit(-1)
    else:
        addr, port = sys.argv[1], sys.argv[2]
        if not (ip_checker(addr) and port_checker(port)):
            print('Invalid IP address or IP port.')
            sys.exit(-1)
    init()
    app = QApplication([])
    main_window = MainWindow()
    with open('./style.qss', 'r', encoding='utf-8') as fp:
        main_window.setStyleSheet(fp.read())
    main_window.show()
    sys.exit(app.exec_())
