from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        super().__init__()
