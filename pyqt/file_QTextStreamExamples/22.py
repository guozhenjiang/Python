def __init__(self, parent):
        super(LicenseTab, self).__init__(parent)
        self.setObjectName('license')
        licensefile = QFile(':/license.html')
        licensefile.open(QFile.ReadOnly | QFile.Text)
        content = QTextStream(licensefile).readAll()
        self.setText(content)
        if sys.platform in {'win32', 'darwin'}:
            self.setStyle(QStyleFactory.create('Fusion')) 