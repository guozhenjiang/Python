def setSection(self, section_box=None):
        if section_box:
            self._section_paramters.setSection(section_box)
            self.section_layout.setCurrentIndex(1)
        else:
            self.section_layout.setCurrentIndex(0)


#if __name__ == '__main__':
#    app = QtWidgets.QApplication([])
#
#    style = QtCore.QFile('./darkStyle.stylesheet')
#    style.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
#    stream = QtCore.QTextStream(style)
#    app.setStyleSheet(stream.readAll())
#
#    section = InstrumentPanel()
#    #section.setFixedHeight(90)
#    section.show()
#
#    app.exec_() 