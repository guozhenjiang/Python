def __init__(self, persepolis_setting):
        super().__init__(persepolis_setting)

        self.persepolis_setting = persepolis_setting

        # setting window size and position
        size = self.persepolis_setting.value(
            'AboutWindow/size', QSize(545, 375))
        position = self.persepolis_setting.value(
            'AboutWindow/position', QPoint(300, 300))

        # read translators.txt files.
        # this file contains all translators.
        f = QFile(':/translators.txt')

        f.open(QIODevice.ReadOnly | QFile.Text)
        f_text = QTextStream(f).readAll()
        f.close()

        self.translators_textEdit.insertPlainText(f_text)



        self.resize(size)
        self.move(position) 