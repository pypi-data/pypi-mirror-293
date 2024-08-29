from PySide6.QtCore import *
from PySide6.QtGui import *
from ez_settings import EZSettings

from .constants import sk

class LogHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        """
        Constructor for the LogHighlighter class.

        :param doc: <QTextDocument> the document to highlight
        """

        self.rules = {}

        for regex, color_list in EZSettings().get(sk.log_highlight_rules, {}).items():
            self.rules[regex] = self.make_format(background_color=QColor(*eval(color_list[0])), foreground_color=QColor(*eval(color_list[1])))

        super().__init__(doc)

    def highlightBlock(self, text: str) -> None:
        """
        Highlights a block of text according to the defined rules.

        :param text: <str> the text to highlight
        """

        for regex, format in self.rules.items():
            i = QRegularExpression(regex).globalMatch(text)
            while i.hasNext():
                match = i.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

    @staticmethod
    def make_format(background_color=Qt.transparent, foreground_color=Qt.white):
        """
        Creates a QTextCharFormat with the specified background and foreground colors.

        :param background_color: <QColor> the background color
        :param foreground_color: <QColor> the foreground color
        :return: <QTextCharFormat> the created format
        """

        if background_color.alpha() == 0:
            background_color = Qt.transparent
        format = QTextCharFormat()
        format.setBackground(background_color)
        format.setForeground(foreground_color)
        return format
