# https://carsonfarmer.com/2009/07/syntax-highlighting-with-pyqt/

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

class MyHighlighter( QSyntaxHighlighter ):
    def __init__( self, parent, theme ):
        QSyntaxHighlighter.__init__( self, parent )
        self.parent = parent
        self.highlightingRules = []

        keyword = QTextCharFormat()
        keyword.setForeground( Qt.darkBlue )
        keyword.setFontWeight( QFont.Bold )
        keywords = QStringList( [ "break", "else", "for", "if", "in",
                                  "next", "repeat", "return", "switch",
                                  "try", "while" ] )
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, keyword )
            self.highlightingRules.append( rule )

            reservedClasses = QTextCharFormat()
            reservedClasses.setForeground( Qt.darkRed )
            reservedClasses.setFontWeight( QFont.Bold )
            keywords = QStringList( [ "array", "character", "complex",
                                    "data.frame", "double", "factor",
                                    "function", "integer", "list",
                                    "logical", "matrix", "numeric",
                                    "vector" ] )
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, reservedClasses )
            
            self.highlightingRules.append( rule )
            assignmentOperator = QTextCharFormat()
            pattern = QRegExp( "(<){1,2}-" )
            assignmentOperator.setForeground( Qt.green )
            assignmentOperator.setFontWeight( QFont.Bold )
            rule = HighlightingRule( pattern, assignmentOperator )
            self.highlightingRules.append( rule )
            number = QTextCharFormat()
            pattern = QRegExp( "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" )
            pattern.setMinimal( True )
            number.setForeground( Qt.blue )
            rule = HighlightingRule( pattern, number )
            self.highlightingRules.append( rule )
            
    def highlightBlock( self, text ):
        for rule in self.highlightingRules:
            expression = QRegExp( rule.pattern )
            index = expression.indexIn( text )
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat( index, length, rule.format )
                index = text.indexOf( expression, index + length )
                self.setCurrentBlockState( 0 )

class TestApp( QMainWindow ):
    def __init__(self):
        QMainWindow.__init__(self)
        editor = QTextEdit()
        highlighter = MyHighlighter( editor )
        self.setCentralWidget( editor )
        self.setWindowTitle( "Syntax Highlighter Example" )


if __name__ == '__main__':
    app = QApplication([])
    test = TestApp()
    test.show()
    sys.exit(app.exec_())