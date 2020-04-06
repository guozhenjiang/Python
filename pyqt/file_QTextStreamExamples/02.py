def setPersepolisColorScheme(self, color_scheme):
        self.persepolis_color_scheme = color_scheme
        if color_scheme == 'Dark Fusion':
            dark_fusion = DarkFusionPalette()
            self.setPalette(dark_fusion)
            file = QFile(":/dark_style.qss")
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

        elif color_scheme == 'Light Fusion':
            dark_fusion = LightFusionPalette()
            self.setPalette(dark_fusion)
            file = QFile(":/light_style.qss")
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())


# create  terminal arguments 