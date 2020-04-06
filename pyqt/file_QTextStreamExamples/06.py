def btmhdwLight():
    # Smart import of the rc file
    import qdarkstyle.pyqt5_style_rc

    # Load the stylesheet content from resources
    from PyQt5.QtCore import QCoreApplication, QFile, QTextStream
    from PyQt5.QtGui import QColor, QPalette
    from qdarkstyle import _apply_palette_fix, _logger

    # Apply palette fix. See issue #139
    _apply_palette_fix(QCoreApplication, QPalette, QColor)

    f = QFile(resource_path("BTMHDW-LIGHT.qss"))
    if not f.exists():
        _logger().error("Unable to load stylesheet, file not found in "
                        "resources")
        return ""
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()

        # Apply OS specific patches
        # stylesheet = _apply_stylesheet_patches(stylesheet)
        return stylesheet