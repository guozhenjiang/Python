def write_demo(self,demo):
        #reading file from QT ressources
        stream = QtCore.QFile(":democfg/{}".format(demo))
        stream.open(QtCore.QIODevice.ReadOnly)
        text=QtCore.QTextStream(stream).readAll()
        stream.close()

        #writting file to disk
        filename="{}/{}".format(self.dir,demo)
        if(Path(filename).exists()):
            #file already exists
            return
            
        filename_handler = open(filename,'w')
        if(filename_handler):
            print("writing filename: "+filename)
            filename_handler.write(text)
            filename_handler.close()
        else:
            mywarning("Cannot open "+filename+" in write mode !!!")

#---------------------------------------------------------------
#-----------------  class MAIN   -----------
#--------------------------------------------------------------- 