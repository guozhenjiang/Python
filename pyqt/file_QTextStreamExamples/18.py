def __init__(self, parent=None):
        super(Changelog, self).__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self.parent = parent
        self.setWindowTitle('{} changelog'.format(qApp.applicationName()))
        changelog = QFile(':/CHANGELOG')
        changelog.open(QFile.ReadOnly | QFile.Text)
        content = QTextStream(changelog).readAll()
        label = QLabel(content, self)
        label.setWordWrap(True)
        label.setTextFormat(Qt.PlainText)
        buttons = QDialogButtonBox(QDialogButtonBox.Close, self)
        buttons.rejected.connect(self.close)
        scrollarea = QScrollArea(self)
        scrollarea.setStyleSheet('QScrollArea { background:transparent; }')
        scrollarea.setWidgetResizable(True)
        scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollarea.setFrameShape(QScrollArea.NoFrame)
        scrollarea.setWidget(label)
        if sys.platform in {'win32', 'darwin'}:
            scrollarea.setStyle(QStyleFactory.create('Fusion'))
        # noinspection PyUnresolvedReferences
        if parent.parent.stylename == 'fusion' or sys.platform in {'win32', 'darwin'}:
            self.setStyleSheet('''
            QScrollArea {{
                background-color: transparent;
                margin-bottom: 10px;
                border: none;
                border-right: 1px solid {};
            }}'''.format('#4D5355' if parent.theme == 'dark' else '#C0C2C3'))
        else:
            self.setStyleSheet('''
            QScrollArea {{
                background-color: transparent;
                margin-bottom: 10px;
                border: none;
            }}''')
        layout = QVBoxLayout()
        layout.addWidget(scrollarea)
        layout.addWidget(buttons)
        self.setLayout(layout)
        self.setMinimumSize(self.sizeHint()) 