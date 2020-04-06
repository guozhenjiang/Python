def load_stylesheet_pyqt5(**kwargs):
    """
    Loads the stylesheet for use in a pyqt5 application.

    :param pyside: True to load the pyside rc file, False to load the PyQt rc file

    :return the stylesheet string
    """
    # Smart import of the rc file

    if kwargs["style"] == "style_Dark":
        import PyQt5_stylesheets.pyqt5_style_Dark_rc
    if kwargs["style"] == "style_DarkOrange":
        import PyQt5_stylesheets.pyqt5_style_DarkOrange_rc
    if kwargs["style"] == "style_Classic":
        import PyQt5_stylesheets.pyqt5_style_Classic_rc

    if kwargs["style"] == "style_navy":
        import PyQt5_stylesheets.pyqt5_style_navy_rc

    if kwargs["style"] == "style_gray":
        import PyQt5_stylesheets.pyqt5_style_gray_rc

    if kwargs["style"] == "style_blue":
        import PyQt5_stylesheets.pyqt5_style_blue_rc

    if kwargs["style"] == "style_black":
        import PyQt5_stylesheets.pyqt5_style_black_rc
    # Load the stylesheet content from resources
    from PyQt5.QtCore import QFile, QTextStream

    f = QFile(":PyQt5_stylesheets/%s.qss"%kwargs["style"])
    if not f.exists():
        f = QFile(":PyQt5_stylesheets/%s.css"%kwargs["style"])
    if not f.exists():
        _logger().error("Unable to load stylesheet, file not found in "
                        "resources")
        return ""
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':  # see issue #12 on github
            mac_fix = '''
            QDockWidget::title
            {
                background-color: #31363b;
                text-align: center;
                height: 12px;
            }
            '''
            stylesheet += mac_fix
        return stylesheet 