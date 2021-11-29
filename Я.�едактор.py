import sys
import os
import sqlite3


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


HTML_EXTENSIONS = ['.htm', '.html']


FONT_SIZES = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 24, 36, 48, 64, 72, 96, 144]

def splitext(p):
    return os.path.splitext(p)[1].lower()


class TextEdit(QTextEdit):
    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()
        if source.hasUrls():
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    break
            else:
                return
        super(TextEdit, self).insertFromMimeData(source)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.editor = TextEdit()
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        font = QFont('Times New Roman', 11)
        self.editor.setFont(font)
        self.editor.setFontPointSize(11)
        self.path = None
        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.menuBar().setNativeMenuBar(False)


        file_toolbar = QToolBar("Действия с файлами")
        file_toolbar.setIconSize(QSize(19, 19))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&Действия с файлами")

        open_file_action = QAction(QIcon(os.path.join('images',
                                                      'open-document.png')),
                                   "Открыть файл...",
                                   self)
        open_file_action.setStatusTip("Открыть файл")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('открыть файл')""")
        con.commit()
        con.close()

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Сохранить", self)
        save_file_action.setStatusTip("Сохранить текущий файл")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('сохранить текущий файл')""")
        con.commit()
        con.close()

        saveas_file_action = QAction(QIcon(os.path.join('images',
                                                        'pencil.png')),
                                     "Сохранить файл как", self)
        saveas_file_action.setStatusTip("Сохранить файл как")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('сохранит файл, как')""")
        con.commit()
        con.close()

        print_action = QAction(QIcon(os.path.join('images',
                                                  'printer.png')),
                               "Распечатать...", self)
        print_action.setStatusTip("Печать документа")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Удобная панель редактирования")
        edit_toolbar.setIconSize(QSize(19, 19))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Удобная панель редактирования")

        cut_action = QAction(QIcon(os.path.join('images',
                                                'scissors.png')),
                             "Вырезать",
                             self)
        cut_action.setStatusTip("Вырезать выбранный текст")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('вырезать выбранный текст')""")
        con.commit()
        con.close()

        copy_action = QAction(QIcon(os.path.join('images',
                                                 'copy.png')),
                              "Копировать",
                              self)
        copy_action.setStatusTip("Копировать выбранный текст")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""
             INSERT INTO Actions(do) VALUES('копировать выбранный текст')""")
        con.commit()
        con.close()

        undo_action = QAction(QIcon(os.path.join('images',
                                                 'undo.png')),
                              "Назад",
                              self)
        undo_action.setStatusTip("Отменить последнее действие")
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images',
                                                 'arrow-continue.png')),
                              "Вперёд",
                              self)
        redo_action.setStatusTip("Восстановить последнее действие")
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""
                   INSERT INTO Actions(do) VALUES('восстановить последнее действие')""")
        con.commit()
        con.close()


        paste_action = QAction(QIcon(os.path.join('images',
                                                  'paste.png')),
                               "Вставить",
                               self)
        paste_action.setStatusTip("Вставить")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""
                      INSERT INTO Actions(do) VALUES('вставить')""")
        con.commit()
        con.close()

        select_action = QAction(QIcon(os.path.join('images',
                                                   'selection.png')),
                                "Выбрать всё",
                                self)
        select_action.setStatusTip("Спорировать весь текст")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute(""" 
          INSERT INTO Actions(do) VALUES('скопировать весь текст')""")
        con.commit()
        con.close()

        self.update_title()
        self.show()

        edit_menu.addSeparator()

        format_toolbar = QToolBar("Форматирование")
        format_toolbar.setIconSize(QSize(19, 19))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Форматирование")

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])

        self.fontsize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)) )
        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(QIcon(os.path.join('images', 'bold.png')), "Полужирный", self)
        self.bold_action.setStatusTip("Полужирный")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('добавить жирности тексту')""")
        con.commit()
        con.close()

        self.italic_action = QAction(QIcon(os.path.join('images', 'italic.png')), "Курсив", self)
        self.italic_action.setStatusTip("Курсив")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('добавить тексту наклон')""")
        con.commit()
        con.close()

        self.underline_action = QAction(QIcon(os.path.join('images', 'underline.png')), "Подчёркнутый", self)
        self.underline_action.setStatusTip("Подчёркнутый")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('подчеркнуть текст')""")
        con.commit()
        con.close()

        format_menu.addSeparator()

        self.alignl_action = QAction(QIcon(os.path.join('images', 'left.png')),
                                     "Выровнять по левому краю", self)
        self.alignl_action.setStatusTip("Выровнять по левому краю")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('выровнять по левому краю')""")
        con.commit()
        con.close()

        self.alignc_action = QAction(QIcon(os.path.join('images', 'center.png')),
                                     "Выровнять по центру", self)
        self.alignc_action.setStatusTip("Выровнять по центру")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('выровнять по центру')""")
        con.commit()
        con.close()

        self.alignr_action = QAction(QIcon(os.path.join('images', 'right.png')),
                                     "Выровнять по правому краю", self)
        self.alignr_action.setStatusTip("Выровнять по правому краю")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('выровнять по правому краю')""")
        con.commit()
        con.close()

        self.alignj_action = QAction(QIcon(os.path.join('images', 'justify.png')),
                                     "Выровнять по ширине", self)
        self.alignj_action.setStatusTip("Выровнять по ширине")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO Actions(do) VALUES('выровнять текст по ширине')""")
        con.commit()
        con.close()

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)
        format_menu.addSeparator()

        self._format_actions = [self.fonts, self.fontsize, self.bold_action, self.italic_action, self.underline_action]
        self.update_format()
        self.update_title()
        self.show()


    def update_format(self):
        # Шрифт выбирается через действительные числа
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.editor.currentFont())
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text documents (*.txt);"
                                                                     "Python Files(*.py);C++ files (*.cpp);"
                                                                        "HTML documents (*.html);"
                                                                     "(All files (*.*)")

        try:
            with open(path) as f:
                text = f.read()
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.editor.setText(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить", "", "Text documents (*.txt);HTML documents (*.html);"
                                                                     "Python Files(*.py);C++ files (*.cpp);"
                                                                     "(All files (*.*);")

        # Возвращает пустую строку при закрытии программы
        if not path:
            return
        text = self.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Я.�едактор" % (os.path.basename(self.path) if self.path else "Безымянный"))

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Я.�едактор")
    window = MainWindow()
    app.exec_()