import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QMessageBox, QSpinBox, QLineEdit, QPushButton, QGridLayout


class EditResultMessageDialog(QDialog):
    def __init__(self, EditPresetRollDialog, ResultMessageIndex, AddMode=False):
        super().__init__(parent=EditPresetRollDialog)

        # Store Parameters
        self.EditPresetRollDialog = EditPresetRollDialog
        self.ResultMessageIndex = ResultMessageIndex

        # Variables
        self.ResultMessage = EditPresetRollDialog.PresetRoll["Result Messages"][self.ResultMessageIndex]
        self.ResultMessageOriginalState = copy.deepcopy(self.ResultMessage)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Labels
        self.PromptLabel = QLabel("Add this result message:" if AddMode else "Edit this result message:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultMinLabel = QLabel("Result Min:")
        self.ResultMaxLabel = QLabel("Result Max:")
        self.ResultTextLabel = QLabel("Result Text:")

        # Inputs
        self.ResultMinSpinBox = QSpinBox()
        self.ResultMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultMinSpinBox.setButtonSymbols(self.ResultMinSpinBox.NoButtons)
        self.ResultMinSpinBox.setRange(-1000000000, 1000000000)
        self.ResultMinSpinBox.setValue(self.ResultMessage["Result Min"])
        self.ResultMinSpinBox.valueChanged.connect(self.UpdateResultMessage)

        self.ResultMaxSpinBox = QSpinBox()
        self.ResultMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultMaxSpinBox.setButtonSymbols(self.ResultMaxSpinBox.NoButtons)
        self.ResultMaxSpinBox.setRange(-1000000000, 1000000000)
        self.ResultMaxSpinBox.setValue(self.ResultMessage["Result Max"])
        self.ResultMaxSpinBox.valueChanged.connect(self.UpdateResultMessage)

        self.ResultTextLineEdit = QLineEdit()
        self.ResultTextLineEdit.setText(self.ResultMessage["Result Text"])
        self.ResultTextLineEdit.textChanged.connect(self.UpdateResultMessage)

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.Layout.addWidget(self.ResultMinLabel, 1, 0)
        self.Layout.addWidget(self.ResultMinSpinBox, 1, 1)
        self.Layout.addWidget(self.ResultMaxLabel, 2, 0)
        self.Layout.addWidget(self.ResultMaxSpinBox, 2, 1)
        self.Layout.addWidget(self.ResultTextLabel, 3, 0)
        self.Layout.addWidget(self.ResultTextLineEdit, 3, 1)
        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 4, 0, 1, 2)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.EditPresetRollDialog.MainWindow.ScriptName)
        self.setWindowIcon(self.EditPresetRollDialog.MainWindow.WindowIcon)

        # Select Text in Result Spin Box
        self.ResultMinSpinBox.selectAll()

        # Execute Dialog
        self.exec_()

    def UpdateResultMessage(self):
        if not self.ValidInput():
            return
        self.ResultMessage["Result Min"] = self.ResultMinSpinBox.value()
        self.ResultMessage["Result Max"] = self.ResultMaxSpinBox.value()
        self.ResultMessage["Result Text"] = self.ResultTextLineEdit.text()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.ResultMessage.update(self.ResultMessageOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.ResultTextLineEdit.text() == "":
            if Alert:
                self.EditPresetRollDialog.MainWindow.DisplayMessageBox("Result message text cannot be blank.", Icon=QMessageBox.Warning, Parent=self)
            return False
        if self.ResultMinSpinBox.value() > self.ResultMaxSpinBox.value():
            if Alert:
                self.EditPresetRollDialog.MainWindow.DisplayMessageBox("Result minimum cannot be greater than result maximum.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
