def set_theme(theme, prefs=None):
    if theme:
        theme = theme.replace(os.pardir, '').replace('.', '')
        theme = theme.join(theme.split()).lower()
        theme_style = resource_path('assets' + os.sep + theme + '_style.qss')
        if not os.path.exists(theme_style):
            theme_style = ':/assets/' + theme + '_style.qss'

        if prefs is not None:
            prefs.put('dwarf_ui_theme', theme)

        try:
            _app = QApplication.instance()
            style_s = QFile(theme_style)
            style_s.open(QFile.ReadOnly)
            style_content = QTextStream(style_s).readAll()
            _app.setStyleSheet(_app.styleSheet() + '\n' + style_content)
        except Exception as e:
            pass
            # err = self.dwarf.spawn(dwarf_args.package, dwarf_args.script) 