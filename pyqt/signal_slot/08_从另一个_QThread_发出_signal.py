import sys                                                                  
from PySide2.QtCore import QObject, Slot, Signal, QThread                                  

# Create the Slots that will receive signals
@Slot(str)
def update_a_str_field(message):
    print(message)

@Slot(int)
def update_a_int_field(self, value):
    print(value)

# Signals must inherit QObject                              
class Communicate(QObject):                                                 
    signal_str = Signal(str)
    signal_int = Signal(int)

class WorkerThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.signals = Communicate()
        # Connect the signals to the main thread slots
        self.signals.signal_str.connect(parent.update_a_str_field)
        self.signals.signal_int.connect(parent.update_a_int_field)

    def run(self):
        self.signals.update_a_int_field.emit(1)
        self.signals.update_a_str_field.emit("Hello World.")