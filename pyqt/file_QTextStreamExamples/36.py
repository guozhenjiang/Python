def __init__(self, _id,_viewer_id, *argv):
    
        super(QtSingleApplication, self).__init__(*argv)
        self._id = _id
        self._viewer_id = _viewer_id
        self._activationWindow = None
        self._activateOnMessage = False

        # Is there another instance running?
        self._outSocket = QLocalSocket()
        self._outSocket.connectToServer(self._id)
        self._isRunning = self._outSocket.waitForConnected(-1)
        

        if self._isRunning:
            # Yes, there is.
            self._outStream = QTextStream(self._outSocket)
            self._outStream.setCodec('UTF-8')
            # Is there another viewer runnging?
            self._outSocketViewer = QLocalSocket()
            self._outSocketViewer.connectToServer(self._viewer_id)
            self._isRunningViewer = self._outSocketViewer.waitForConnected(-1)
            if self._isRunningViewer:
                self._outStreamViewer = QTextStream(self._outSocketViewer)
                self._outStreamViewer.setCodec('UTF-8')
            else:
                # app is running, we announce us as viewer app
                # First we remove existing servers of that name that might not have been properly closed as the server died
                QLocalServer.removeServer(self._viewer_id) 
                self._outSocketViewer = None
                self._outStreamViewer = None
                self._inSocket = None
                self._inStream = None
                self._server = QLocalServer()
                self._server.listen(self._viewer_id)
                self._server.newConnection.connect(self._onNewConnection)
        else:
            self._isRunningViewer = False
            # No, there isn't.
            # First we remove existing servers of that name that might not have been properly closed as the server died
            QLocalServer.removeServer(self._id) 
            self._outSocket = None
            self._outStream = None
            self._inSocket = None
            self._inStream = None
            self._server = QLocalServer()
            self._server.listen(self._id)
            self._server.newConnection.connect(self._onNewConnection) 