def __init__(self, appid, *argv):
        super(SingleApplication, self).__init__(*argv)
        self._appid = appid
        self._activationWindow = None
        self._activateOnMessage = False
        self._outSocket = QLocalSocket()
        self._outSocket.connectToServer(self._appid)
        self._isRunning = self._outSocket.waitForConnected()
        self._outStream = None
        self._inSocket = None
        self._inStream = None
        self._server = None
        self.settings = QSettings(SingleApplication.getSettingsPath(), QSettings.IniFormat)
        self.singleInstance = self.settings.value('singleInstance', 'on', type=str) in {'on', 'true'}
        if self._isRunning and self.singleInstance:
            self._outStream = QTextStream(self._outSocket)
            for a in argv[0][1:]:
                a = os.path.join(os.getcwd(), a)
                if os.path.isfile(a):
                    self.sendMessage(a)
                    break
            sys.exit(0)
        else:
            error = self._outSocket.error()
            if error == QLocalSocket.ConnectionRefusedError:
                self.close()
                QLocalServer.removeServer(self._appid)
            self._outSocket = None
            self._server = QLocalServer()
            self._server.listen(self._appid)
            self._server.newConnection.connect(self._onNewConnection) 