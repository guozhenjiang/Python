def openFile(self):
        if settings.get("file_dialog_dir"):
            self.curDir = '~/'
        else:
            self.curDir = settings.get("file_dialog_dir")
        fn = QFileDialog.getOpenFileName(self,
                self.tr("Open File..."), self.curDir,
                self.tr("HTML-Files (*.htm *.html);;All Files (*)"))
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if fn:
            self.lastFolder = os.path.dirname(fn)
            if os.path.exists(fn):
                if os.path.isfile(fn):
                    f = QFile(fn)
                    if not f.open(QIODevice.ReadOnly |
                                  QIODevice.Text):
                        QtGui.QMessageBox.information(self.parent(),
                        self.tr("Error - Lector"),
                        self.tr("Can't open '%s.'" % fn))
                    else:
                        stream = QTextStream(f)
                        text = stream.readAll()
                        self.setText(text)
                else:
                    QMessageBox.information(self.parent(),
                    self.tr("Error - Lector"),
                    self.tr("'%s' is not a file." % fn))
        QApplication.restoreOverrideCursor() 