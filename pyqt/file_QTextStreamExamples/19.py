def loadQSS(theme) -> None:
        filename = ':/styles/{}.qss'.format(theme)
        if QFileInfo(filename).exists():
            qssfile = QFile(filename)
            qssfile.open(QFile.ReadOnly | QFile.Text)
            content = QTextStream(qssfile).readAll()
            qApp.setStyleSheet(content) 