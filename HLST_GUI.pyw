import os
import subprocess
import sys
import webbrowser

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

if sys.platform != "win32":
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Platform Error")
    msg.setText("This tool only works on Windows.")
    msg.exec()
    sys.exit(1)

BG_COLOR = "#005780"
TEXT_COLOR = "#FFFFFF"
SAVED_GAMES_COLOR = "#1C6A8E"
RENAME_COLOR = "#397C9C"
DECOMPRESS_COLOR = "#558FAA"
EDITOR_COLOR = "#71A2B8"
LEGILIMENS_COLOR = "#8EB4C7"
COMPRESS_COLOR = "#AAC7D5"

BUTTON_RADIUS = 10


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def _draw_outlined_text(painter, rect, text, font, align=Qt.AlignmentFlag.AlignCenter):
    painter.save()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    path = QPainterPath()
    path.addText(0, 0, font, text)

    fm = painter.fontMetrics()
    text_w = fm.horizontalAdvance(text)
    text_h = fm.ascent()

    if align & Qt.AlignmentFlag.AlignHCenter:
        x = rect.x() + (rect.width() - text_w) / 2
    elif align & Qt.AlignmentFlag.AlignRight:
        x = rect.right() - text_w
    else:
        x = rect.x()

    if align & Qt.AlignmentFlag.AlignVCenter:
        y = rect.y() + (rect.height() + text_h) / 2 - fm.descent()
    else:
        y = rect.y() + text_h

    path.translate(x, y)

    outline_color = QColor(0, 0, 0, 140)
    pen = QPen(outline_color, 2.0)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.strokePath(path, pen)

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(TEXT_COLOR))
    painter.drawPath(path)

    painter.restore()


class OutlinedLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRectF(self.contentsRect())
        _draw_outlined_text(
            painter,
            rect,
            self.text(),
            self.font(),
            self.alignment(),
        )
        painter.end()


class OutlinedButton(QPushButton):
    def __init__(self, text, bg, hover, parent=None):
        super().__init__(text, parent)
        self._bg = QColor(bg)
        self._hover = QColor(hover)
        self._hovered = False
        self._pressed = False
        self.setMinimumHeight(56)
        self.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._hover if self._hovered else self._bg
        if self._pressed:
            color = self._bg.darker(115)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect(), BUTTON_RADIUS, BUTTON_RADIUS)

        _draw_outlined_text(
            painter,
            QRectF(self.rect()),
            self.text(),
            self.font(),
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter,
        )
        painter.end()


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Version 2.3 © Henry & Lukas 2025-2026")
        self.setFixedSize(640, 720)
        self._center_window()

        root = QWidget()
        root.setStyleSheet(f"background-color: {BG_COLOR};")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 30, 0, 25)
        outer.setSpacing(0)

        title = OutlinedLabel("HOGWARTS LEGACY SAVE TOOLS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setContentsMargins(0, 0, 0, 20)
        title.setMinimumHeight(50)
        outer.addWidget(title)

        layout = QVBoxLayout()
        layout.setContentsMargins(80, 0, 80, 0)
        layout.setSpacing(10)
        outer.addLayout(layout)

        buttons = [
            ("GO TO SAVED GAMES", SAVED_GAMES_COLOR, "#165570", self.go_to_saved_games),
            ("RENAME", RENAME_COLOR, "#2E637D", self.rename_sav),
            ("DECOMPRESS", DECOMPRESS_COLOR, "#44728C", self.decompress_in_terminal),
            ("LAUNCH THE EDITOR", EDITOR_COLOR, "#5B8294", self.launch_editor),
            ("LAUNCH LEGILIMENS", LEGILIMENS_COLOR, "#7190A0", self.launch_legilimens),
            ("COMPRESS", COMPRESS_COLOR, "#889FA8", self.compress_in_terminal),
        ]
        for text, bg, hover, slot in buttons:
            btn = OutlinedButton(text, bg, hover)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        self.logbox.setFont(QFont("Consolas", 10))
        self.logbox.setStyleSheet("""
            QTextEdit {
                background-color: #003350;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }
        """)
        self.logbox.setMinimumHeight(160)
        layout.addWidget(self.logbox, stretch=1)

        self.log("Ready")

    def _center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 500) // 2
        y = (screen.height() - 768) // 2
        self.move(x, y)

    def log(self, msg):
        self.logbox.append(msg)

    def _error(self, title, text):
        QMessageBox.critical(self, title, text)

    def _warning(self, title, text):
        QMessageBox.warning(self, title, text)

    def _ask(self, title, text):
        reply = QMessageBox.question(
            self,
            title,
            text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

    def go_to_saved_games(self):
        saved_games_path = os.path.expandvars(
            r"%LocalAppData%\Hogwarts Legacy\Saved\SaveGames"
        )
        self.log(f"Opening folder: {saved_games_path}")
        if os.path.isdir(saved_games_path):
            try:
                os.startfile(saved_games_path)
            except Exception as e:
                self.log(f"Error opening folder: {e}")
                self._error("Error", f"Could not open folder:\n{e}")
        else:
            self.log("Save folder not found!")
            self._warning(
                "Folder Not Found",
                "Hogwarts Legacy save folder does not exist.\n"
                "Make sure the game has been launched at least once.",
            )

    def rename_sav(self):
        self.log("Select .sav to rename to .orig")
        path, _ = QFileDialog.getOpenFileName(
            self, "Select save file", "", "Save file (*.sav)"
        )
        if not path or not path.lower().endswith(".sav"):
            self.log("Cancelled")
            return

        new_path = path[:-4] + ".orig"
        if os.path.exists(new_path):
            if not self._ask(
                "Overwrite?",
                f"{os.path.basename(new_path)} already exists. Overwrite?",
            ):
                self.log("Rename cancelled: file exists")
                return

        try:
            os.rename(path, new_path)
            self.log(f"Renamed to: {os.path.basename(new_path)}")
        except Exception as e:
            self.log(f"Error renaming: {e}")

    def decompress_in_terminal(self):
        self.log("Select .orig file to decompress")
        orig, _ = QFileDialog.getOpenFileName(
            self, "Select orig save", "", "Orig save (*.orig)"
        )
        if not orig or not orig.lower().endswith(".orig"):
            self.log("Cancelled")
            return

        folder = os.path.dirname(orig)
        base = os.path.basename(orig)
        decomp = base[:-5] + ".decomp"

        hlsaves_exe = get_resource_path("hlsaves.exe")
        if not os.path.isfile(hlsaves_exe):
            self.log("ERROR: hlsaves.exe not found in application directory")
            return

        try:
            subprocess.Popen(
                [hlsaves_exe, "-d", base, decomp],
                cwd=folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.log(f"Decompressing → {decomp}")
        except Exception as e:
            self.log(f"Failed to start decompression: {e}")

    def launch_editor(self):
        html_path = get_resource_path("hlse.html")
        if os.path.isfile(html_path):
            self.log("Opening Hogwarts Legacy Save Game Editor (hlse.html)")
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
        else:
            self.log("ERROR: hlse.html not found in application directory")

    def launch_legilimens(self):
        self.log("Select input file for Legilimens")
        input_file, _ = QFileDialog.getOpenFileName(
            self, "Select file for Legilimens", "", "All files (*.*)"
        )
        if not input_file:
            self.log("Cancelled")
            return

        folder = os.path.dirname(input_file)
        input_fullpath = os.path.abspath(input_file)
        legilimens_exe = get_resource_path("Legilimens.exe")

        if not os.path.isfile(legilimens_exe):
            self.log("ERROR: Legilimens.exe not found in application directory")
            return

        output_file = "output.txt"
        try:
            subprocess.Popen(
                [legilimens_exe, input_fullpath, "--filters", "ALL", "-o", output_file],
                cwd=folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.log(f"Running Legilimens → {os.path.join(folder, output_file)}")
        except Exception as e:
            self.log(f"Failed to launch Legilimens: {e}")

    def compress_in_terminal(self):
        self.log("Select .edited file to compress")
        edited, _ = QFileDialog.getOpenFileName(
            self, "Select edited save", "", "Edited save (*.edited)"
        )
        if not edited or not edited.lower().endswith(".edited"):
            self.log("Cancelled")
            return

        folder = os.path.dirname(edited)
        base = os.path.basename(edited)
        sav = base[:-7] + ".sav"

        hlsaves_exe = get_resource_path("hlsaves.exe")
        if not os.path.isfile(hlsaves_exe):
            self.log("ERROR: hlsaves.exe not found in application directory")
            return

        try:
            subprocess.Popen(
                [hlsaves_exe, "-c", base, sav],
                cwd=folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.log(f"Compressing → {sav}")
        except Exception as e:
            self.log(f"Failed to start compression: {e}")

    def on_closing(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
