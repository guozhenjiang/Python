def __init__(self, parent=None):
        super(QuantumPT, self).__init__(parent)

        Registry.create()

        # self.style = 0
        self.modify_style.connect(self.change_style)

        # Initialize language manager
        LanguageManager(language='en_US')

        # Add predefined fonts
        QFontDatabase.addApplicationFont(":/fonts/besmellah.ttf")
        QFontDatabase.addApplicationFont(":/fonts/capsuula.ttf")
        QFontDatabase.addApplicationFont(":/fonts/ubuntu.ttf")

        # Set stylesheet as Qt resource
        stylesheet = QFile(":/styles/default.css")
        stylesheet.open(QFile.ReadOnly | QFile.Text)

        self.stylesheet = QTextStream(stylesheet).readAll()
        self.setStyleSheet(self.stylesheet)

        # Use ico file so it can handle multiple sizes
        self.setWindowIcon(QIcon(":/icons/app.ico"))

        self.setApplicationDisplayName("QuantumPrayerTimes")
        self.setApplicationName("QuantumPrayerTimes")

        self.setOrganizationName('QuantumPrayerTimes')
        self.setOrganizationDomain('quantumprayertimes.github.io')

        self.setEffectEnabled(Qt.UI_AnimateCombo, False)
        self.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        Registry().register_signal("change_style", self.modify_style) 