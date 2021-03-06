from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QSizePolicy

from Interface.Widgets.DieTypeSpinBox import DieTypeSpinBox


class CreateDieClockDialog(QDialog):
    def __init__(self, MainWindow):
        super().__init__(parent=MainWindow)

        # Store Parameters
        self.MainWindow = MainWindow

        # Variables
        self.Submitted = False
        self.Name = None
        self.DieType = None
        self.ComplicationThreshold = None

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Labels
        self.PromptLabel = QLabel("Create a die clock:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NameLabel = QLabel("Name:")
        self.DieTypeLabel = QLabel("Die Type:")
        self.ComplicationThresholdLabel = QLabel("Complication Threshold:")

        # Inputs
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setSizePolicy(self.InputsSizePolicy)
        self.NameLineEdit.setText("New Die Clock")

        self.DieTypeSpinBox = DieTypeSpinBox()
        self.DieTypeSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DieTypeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DieTypeSpinBox.setButtonSymbols(self.DieTypeSpinBox.NoButtons)
        self.DieTypeSpinBox.setRange(1, 1000000000)
        self.DieTypeSpinBox.setValue(20)

        self.ComplicationThresholdSpinBox = QSpinBox()
        self.ComplicationThresholdSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ComplicationThresholdSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ComplicationThresholdSpinBox.setButtonSymbols(self.ComplicationThresholdSpinBox.NoButtons)
        self.ComplicationThresholdSpinBox.setRange(1, 1000000000)
        self.ComplicationThresholdSpinBox.setValue(5)

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.DoneButton.setDefault(True)
        self.DoneButton.setAutoDefault(True)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0)

        self.NameLayout = QGridLayout()
        self.NameLayout.addWidget(self.NameLabel, 0, 0)
        self.NameLayout.addWidget(self.NameLineEdit, 0, 1)
        self.NameLayout.setColumnStretch(1, 1)
        self.Layout.addLayout(self.NameLayout, 1, 0)

        self.DieTypeLayout = QGridLayout()
        self.DieTypeLayout.addWidget(self.DieTypeLabel, 0, 0)
        self.DieTypeLayout.addWidget(self.DieTypeSpinBox, 0, 1)
        self.DieTypeLayout.setColumnStretch(1, 1)
        self.Layout.addLayout(self.DieTypeLayout, 2, 0)

        self.ComplicationThresholdLayout = QGridLayout()
        self.ComplicationThresholdLayout.addWidget(self.ComplicationThresholdLabel, 0, 0)
        self.ComplicationThresholdLayout.addWidget(self.ComplicationThresholdSpinBox, 0, 1)
        self.ComplicationThresholdLayout.setColumnStretch(1, 1)
        self.Layout.addLayout(self.ComplicationThresholdLayout, 3, 0)

        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 4, 0)

        for Row in [1, 2, 3]:
            self.Layout.setRowStretch(Row, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.MainWindow.ScriptName)
        self.setWindowIcon(self.MainWindow.WindowIcon)

        # Select Text in Name Line Edit
        self.NameLineEdit.selectAll()

        # Execute Dialog
        self.exec_()

    def Done(self):
        if self.ValidInput(Alert=True):
            self.Submitted = True
            self.Name = self.NameLineEdit.text()
            self.DieType = self.DieTypeSpinBox.value()
            self.ComplicationThreshold = self.ComplicationThresholdSpinBox.value()
            self.close()

    def Cancel(self):
        self.close()

    def ValidInput(self, Alert=False):
        if self.NameLineEdit.text() == "":
            if Alert:
                self.MainWindow.DisplayMessageBox("Die clocks must have a name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        ComplicationThreshold = self.ComplicationThresholdSpinBox.value()
        if ComplicationThreshold < 1 or ComplicationThreshold >= self.DieTypeSpinBox.value():
            if Alert:
                self.MainWindow.DisplayMessageBox("Complication threshold must be greater than 0 and lesser than the die type.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
