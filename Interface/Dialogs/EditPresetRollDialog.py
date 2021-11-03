import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton, QSpinBox, QSizePolicy, QMessageBox

from Interface.Widgets.DieTypeSpinBox import DieTypeSpinBox
from Interface.Widgets.ResultMessagesTreeWidget import ResultMessagesTreeWidget


class EditPresetRollDialog(QDialog):
    def __init__(self, DiceRollerWindow, PresetRollIndex, AddMode=False):
        super().__init__(parent=DiceRollerWindow)

        # Store Parameters
        self.DiceRollerWindow = DiceRollerWindow
        self.PresetRollIndex = PresetRollIndex

        # Variables
        self.PresetRoll = self.DiceRollerWindow.DiceRoller.PresetRolls[self.PresetRollIndex]
        self.PresetRollOriginalState = copy.deepcopy(self.PresetRoll)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Labels
        self.PromptLabel = QLabel("Add this preset roll:" if AddMode else "Edit this preset roll:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NameLabel = QLabel("Name:")
        self.DieTypeLabel = QLabel("d")
        self.ModifierLabel = QLabel("+")
        self.ResultMessagesLabel = QLabel("Result Messages:")
        self.ResultMessagesLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Roll Inputs
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setText(self.PresetRoll["Name"])
        self.NameLineEdit.textChanged.connect(self.UpdatePresetRoll)

        self.DiceNumberSpinBox = QSpinBox()
        self.DiceNumberSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DiceNumberSpinBox.setButtonSymbols(self.DiceNumberSpinBox.NoButtons)
        self.DiceNumberSpinBox.setRange(1, 1000000000)
        self.DiceNumberSpinBox.setValue(self.PresetRoll["Dice Number"])
        self.DiceNumberSpinBox.valueChanged.connect(self.UpdatePresetRoll)

        self.DieTypeSpinBox = DieTypeSpinBox()
        self.DieTypeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DieTypeSpinBox.setButtonSymbols(self.DieTypeSpinBox.NoButtons)
        self.DieTypeSpinBox.setRange(1, 1000000000)
        self.DieTypeSpinBox.setValue(self.PresetRoll["Die Type"])
        self.DieTypeSpinBox.valueChanged.connect(self.UpdatePresetRoll)

        self.ModifierSpinBox = QSpinBox()
        self.ModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ModifierSpinBox.setButtonSymbols(self.ModifierSpinBox.NoButtons)
        self.ModifierSpinBox.setRange(-1000000000, 1000000000)
        self.ModifierSpinBox.setValue(self.PresetRoll["Modifier"])
        self.ModifierSpinBox.valueChanged.connect(self.UpdatePresetRoll)

        # Result Messages Tree Widget
        self.ResultMessagesTreeWidget = ResultMessagesTreeWidget(self)

        # Buttons
        self.AddResultMessageButton = QPushButton("+")
        self.AddResultMessageButton.clicked.connect(self.AddResultMessage)
        self.AddResultMessageButton.setSizePolicy(self.InputsSizePolicy)
        self.DeleteResultMessageButton = QPushButton("-")
        self.DeleteResultMessageButton.clicked.connect(self.DeleteResultMessage)
        self.DeleteResultMessageButton.setSizePolicy(self.InputsSizePolicy)
        self.EditResultMessageButton = QPushButton("Edit")
        self.EditResultMessageButton.clicked.connect(self.EditResultMessage)
        self.EditResultMessageButton.setSizePolicy((self.InputsSizePolicy))
        self.CopyResultMessageButton = QPushButton("Copy")
        self.CopyResultMessageButton.clicked.connect(self.CopyResultMessage)
        self.CopyResultMessageButton.setSizePolicy((self.InputsSizePolicy))
        self.ResultMessageMoveUpButton = QPushButton("\u2191")
        self.ResultMessageMoveUpButton.clicked.connect(self.MoveResultMessageUp)
        self.ResultMessageMoveUpButton.setSizePolicy(self.InputsSizePolicy)
        self.ResultMessageMoveDownButton = QPushButton("\u2193")
        self.ResultMessageMoveDownButton.clicked.connect(self.MoveResultMessageDown)
        self.ResultMessageMoveDownButton.setSizePolicy(self.InputsSizePolicy)
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.DoneButton.setDefault(True)
        self.DoneButton.setAutoDefault(True)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.NameLayout = QGridLayout()
        self.NameLayout.addWidget(self.NameLabel, 0, 0)
        self.NameLayout.addWidget(self.NameLineEdit, 0, 1)
        self.NameLayout.setColumnStretch(1, 1)
        self.Layout.addLayout(self.NameLayout, 1, 0, 1, 2)
        self.DiceInputsLayout = QGridLayout()
        self.DiceInputsLayout.addWidget(self.DiceNumberSpinBox, 0, 0)
        self.DiceInputsLayout.addWidget(self.DieTypeLabel, 0, 1)
        self.DiceInputsLayout.addWidget(self.DieTypeSpinBox, 0, 2)
        self.DiceInputsLayout.addWidget(self.ModifierLabel, 0, 3)
        self.DiceInputsLayout.addWidget(self.ModifierSpinBox, 0, 4)
        self.DiceInputsLayout.setColumnStretch(0, 1)
        self.DiceInputsLayout.setColumnStretch(2, 1)
        self.DiceInputsLayout.setColumnStretch(4, 1)
        self.Layout.addLayout(self.DiceInputsLayout, 2, 0, 1, 2)
        self.ResultMessagesLayout = QGridLayout()
        self.ResultMessagesLayout.addWidget(self.ResultMessagesLabel, 0, 0)
        self.ResultMessagesLayout.addWidget(self.ResultMessagesTreeWidget, 1, 0, 6, 1)
        self.ResultMessagesLayout.addWidget(self.AddResultMessageButton, 1, 1)
        self.ResultMessagesLayout.addWidget(self.DeleteResultMessageButton, 2, 1)
        self.ResultMessagesLayout.addWidget(self.EditResultMessageButton, 3, 1)
        self.ResultMessagesLayout.addWidget(self.CopyResultMessageButton, 4, 1)
        self.ResultMessagesLayout.addWidget(self.ResultMessageMoveUpButton, 5, 1)
        self.ResultMessagesLayout.addWidget(self.ResultMessageMoveDownButton, 6, 1)
        self.ResultMessagesLayout.setRowStretch(1, 1)
        self.ResultMessagesLayout.setRowStretch(2, 1)
        self.ResultMessagesLayout.setRowStretch(3, 1)
        self.ResultMessagesLayout.setRowStretch(4, 1)
        self.ResultMessagesLayout.setRowStretch(5, 1)
        self.ResultMessagesLayout.setRowStretch(6, 1)
        self.Layout.addLayout(self.ResultMessagesLayout, 3, 0, 1, 2)
        self.Layout.addWidget(self.DoneButton, 4, 0)
        self.Layout.addWidget(self.CancelButton, 4, 1)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.DiceRollerWindow.ScriptName)
        self.setWindowIcon(self.DiceRollerWindow.WindowIcon)

        # Update Display
        self.UpdateDisplay()

        # Execute Dialog
        self.exec_()

    def AddResultMessage(self):
        pass

    def DeleteResultMessage(self):
        pass

    def EditResultMessage(self):
        pass

    def CopyResultMessage(self):
        pass

    def MoveResultMessageUp(self):
        self.MoveResultMessage(-1)

    def MoveResultMessageDown(self):
        self.MoveResultMessage(1)

    def MoveResultMessage(self, Delta):
        pass

    def UpdatePresetRoll(self):
        self.PresetRoll["Name"] = self.NameLineEdit.text()
        self.PresetRoll["Dice Number"] = self.DiceNumberSpinBox.value()
        self.PresetRoll["Die Type"] = self.DieTypeSpinBox.value()
        self.PresetRoll["Modifier"] = self.ModifierSpinBox.value()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput():
            self.close()

    def Cancel(self):
        self.DiceRollerWindow.DiceRoller.PresetRolls[self.PresetRollIndex] = self.PresetRollOriginalState
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self):
        if self.NameLineEdit.text() == "":
            self.DiceRollerWindow.DisplayMessageBox("Preset rolls must have a name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True

    def UpdateDisplay(self):
        self.ResultMessagesTreeWidget.FillFromResultMessages()