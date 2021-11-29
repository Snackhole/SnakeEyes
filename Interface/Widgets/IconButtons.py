from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class AddButton(QPushButton):
    def __init__(self, Slot, Tooltip="Add"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAe0lEQVQ4jWP8//8/AxrAEEADjMhcFmwqbOrFsOo80vgKQwyrASCgZCuEwr93+B1WdUwEnEsQsBDhZ3SAoh7sBVx+Rgfo6kBhAg8DdD+jA1xhQnEYDLwB8DBAj2di0wHYAPQURmpKREnbpOYF6oUBOsDlZwznUJSdGRgYAHP6JbnRUVuCAAAAAElFTkSuQmCC"))
        self.setIcon(QIcon(IconPixmap))


class CopyButton(QPushButton):
    def __init__(self, Slot, Tooltip="Copy"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAf0lEQVQ4jWP8////fwbiASO6ShYQYVMvRtCEI42vMNQdbXoNMQAElGyFcGq+d/gdTjkmEpxPGwNYiFADB0caX6EGeCMeA9D9jS2gQQGL1wXEBCz1wgBfVBE0AOQXdEBM4oIZwIiuGCO08YBBnpCICVhQdmZgZETNpURncQYGBgDHRSyJhgjGSwAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))


class DeleteButton(QPushButton):
    def __init__(self, Slot, Tooltip="Delete"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAQ0lEQVQ4jWMYBQyM/////09JMLCAiHoxMbI0N756BTEABGyFhEjSfPjdOzDNRJbVSGDgDYCHAcxPpAKKo3HEAwYGBgADWhCsPEB/zAAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))


class EditButton(QPushButton):
    def __init__(self, Slot, Tooltip="Edit"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAuElEQVQ4jZ2SsQ6DMAxEz1VF1XZB4n+694vZ+R8kFkCwXIcQyy7QJD3JkqPknR0nQhKZsgclJpcSWETcOtdA4blbdiYpAwcD2Jn8MlB46CvcXzfdcCYkj4IM0+XQVxoAOHcLAxYkB6/gKgNA3awuN4x8X6EIBvwQi2Fr8BfsOhARTGOLulkBIAuOBm6K1iQFA4CQZKxu9Xi+kzCA8KBbF5zGVnMj/R+G0dAO7Kbt8LTypusBlAVGfQDRP71h3nr/pAAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))


class MoveDownButton(QPushButton):
    def __init__(self, Slot, Tooltip="Move Down"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAj0lEQVQ4jWP8//8/AxrAEEADjMhcFmwqxBTqsep89aARQwyrASAg5GWLwn+37TBWdUwEnEsQDAMDWIiINnSAoh4cC7iiDR2gqwNFKzwa0aMNHeCKViaYSbjiGRsAqYUlKiZY0iTWEGTNIL2wWCDKEHTNcC8QYwg2zWAGrtyILcTRNeMyAG4IFoCimYGBgQEAtDVEATWWeH0AAAAASUVORK5CYII="))
        self.setIcon(QIcon(IconPixmap))


class MoveUpButton(QPushButton):
    def __init__(self, Slot, Tooltip="Move Up"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAkklEQVQ4jWP8//8/AxaAVZCBgYERXYAFl2YxhXoUwVcPGmFyKIaguwCuWcjLFsWAd9sOwwxBcQkTMZpBACSG5Cq4rUzEaMZnCBOxmnEZwkSKZmyGwGMBFEjoipABujwMgA1ACl0GBixRCAPo6mAuQE8cuBIRDKCoZ8KrlAgwDAzAlpnAAFe0oQNs2Zn4WGBgYAAAciE1ohhWgxkAAAAASUVORK5CYII="))
        self.setIcon(QIcon(IconPixmap))


class RollButton(QPushButton):
    def __init__(self, Slot, Tooltip="Roll"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAATElEQVQ4jWP8////fwYKAAsDAwMDIyMjWZr///8PMQDGIQXALGXCJoHNRbjEMQwgFbCgC+DyCi5xil0wGgbDIgzgBpCboVjwmU4MAACMcR88hf4SzwAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))
