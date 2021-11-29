import copy
import json
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, QGridLayout, QFrame, QLabel, QTextEdit, QSpinBox, QMessageBox, QAction, QInputDialog

from Core.DiceRoller import DiceRoller
from Interface.Dialogs.CreateDieClockDialog import CreateDieClockDialog
from Interface.Dialogs.EditPresetRollDialog import EditPresetRollDialog
from Interface.Widgets.DieTypeSpinBox import DieTypeSpinBox
from Interface.Widgets.IconButtons import AddButton, CopyButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton, RollButton
from Interface.Widgets.PresetRollsTreeWidget import PresetRollsTreeWidget
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class MainWindow(QMainWindow, SaveAndOpenMixin):
    # Initialization Methods
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        super().__init__()

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".snakeeyes", "SnakeEyes Dice Roller", (DiceRoller,))

        # Create Dice Roller
        self.DiceRoller = DiceRoller()

        # Create Interface
        self.CreateInterface()
        self.show()

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        # Load Theme
        self.LoadTheme()

        # Window Icon and Title
        self.WindowIcon = QIcon(self.GetResourcePath("Assets/SnakeEyes Icon.png"))
        self.setWindowIcon(self.WindowIcon)
        self.UpdateWindowTitle()

        # Styles
        self.RollLabelStyle = "QLabel {font-size: 16pt;}"
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold}"
        self.SpinBoxStyle = "QSpinBox {font-size: 16pt;}"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Dice Roller Width
        self.DiceRollerWidth = 80

        # Dice Number Spin Box
        self.DiceNumberSpinBox = QSpinBox()
        self.DiceNumberSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DiceNumberSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.DiceNumberSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DiceNumberSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.DiceNumberSpinBox.setButtonSymbols(self.DiceNumberSpinBox.NoButtons)
        self.DiceNumberSpinBox.setRange(1, 1000000000)

        # Die Type Label
        self.DieTypeLabel = QLabel("d")
        self.DieTypeLabel.setStyleSheet(self.RollLabelStyle)
        self.DieTypeLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Die Type Spin Box
        self.DieTypeSpinBox = DieTypeSpinBox()
        self.DieTypeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DieTypeSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.DieTypeSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DieTypeSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.DieTypeSpinBox.setButtonSymbols(self.DieTypeSpinBox.NoButtons)
        self.DieTypeSpinBox.setRange(1, 1000000000)

        # Modifier Label
        self.ModifierLabel = QLabel("+")
        self.ModifierLabel.setStyleSheet(self.RollLabelStyle)
        self.ModifierLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Modifier Spin Box
        self.ModifierSpinBox = QSpinBox()
        self.ModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ModifierSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.ModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ModifierSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.ModifierSpinBox.setButtonSymbols(self.ModifierSpinBox.NoButtons)
        self.ModifierSpinBox.setRange(-1000000000, 1000000000)

        # Roll Button
        self.RollButton = RollButton(lambda: self.RollAction.trigger(), "Roll")
        self.RollButton.setSizePolicy(self.InputsSizePolicy)

        # Preset Rolls Label
        self.PresetRollsLabel = QLabel("Preset Rolls")
        self.PresetRollsLabel.setStyleSheet(self.SectionLabelStyle)
        self.PresetRollsLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Preset Rolls Tree Widget
        self.PresetRollsTreeWidget = PresetRollsTreeWidget(self)
        self.PresetRollsTreeWidget.itemActivated.connect(lambda: self.RollPresetRollAction.trigger())

        # Preset Rolls Buttons
        self.PresetRollsRollButton = RollButton(lambda: self.RollPresetRollAction.trigger(), "Roll Preset Roll")
        self.PresetRollsRollButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsAddButton = AddButton(self.AddPresetRoll, "Add Preset Roll")
        self.PresetRollsAddButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsDeleteButton = DeleteButton(self.DeletePresetRoll, "Delete Preset Roll")
        self.PresetRollsDeleteButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsEditButton = EditButton(self.EditPresetRoll, "Edit Preset Roll")
        self.PresetRollsEditButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsCopyButton = CopyButton(self.CopyPresetRoll, "Copy Preset Roll")
        self.PresetRollsCopyButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsMoveUpButton = MoveUpButton(self.MovePresetRollUp, "Move Preset Roll Up")
        self.PresetRollsMoveUpButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsMoveDownButton = MoveDownButton(self.MovePresetRollDown, "Move Preset Roll Down")
        self.PresetRollsMoveDownButton.setSizePolicy(self.InputsSizePolicy)

        # Results Log Label
        self.ResultsLogLabel = QLabel("Results Log")
        self.ResultsLogLabel.setStyleSheet(self.SectionLabelStyle)
        self.ResultsLogLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Results Log Text Edit
        self.ResultsLogTextEdit = QTextEdit()
        self.ResultsLogTextEdit.setReadOnly(True)

        # Create Layout
        self.Layout = QGridLayout()

        # Dice Roller Inputs in Layout
        self.DiceRollerInputsLayout = QGridLayout()
        self.DiceRollerInputsLayout.addWidget(self.DiceNumberSpinBox, 0, 0)
        self.DiceRollerInputsLayout.addWidget(self.DieTypeLabel, 0, 1)
        self.DiceRollerInputsLayout.addWidget(self.DieTypeSpinBox, 0, 2)
        self.DiceRollerInputsLayout.addWidget(self.ModifierLabel, 0, 3)
        self.DiceRollerInputsLayout.addWidget(self.ModifierSpinBox, 0, 4)
        self.DiceRollerInputsLayout.addWidget(self.RollButton, 0, 5)
        self.Layout.addLayout(self.DiceRollerInputsLayout, 0, 0)

        # Preset Rolls in Layout
        self.PresetRollsLayout = QGridLayout()
        self.PresetRollsLayout.addWidget(self.PresetRollsLabel, 0, 0, 1, 7)
        self.PresetRollsLayout.addWidget(self.PresetRollsRollButton, 1, 0)
        self.PresetRollsLayout.addWidget(self.PresetRollsAddButton, 1, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsDeleteButton, 1, 2)
        self.PresetRollsLayout.addWidget(self.PresetRollsEditButton, 1, 3)
        self.PresetRollsLayout.addWidget(self.PresetRollsCopyButton, 1, 4)
        self.PresetRollsLayout.addWidget(self.PresetRollsMoveUpButton, 1, 5)
        self.PresetRollsLayout.addWidget(self.PresetRollsMoveDownButton, 1, 6)
        self.PresetRollsLayout.addWidget(self.PresetRollsTreeWidget, 2, 0, 1, 7)
        self.PresetRollsLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.PresetRollsLayout, 1, 0)

        # Results Log Widgets in Layout
        self.ResultsLogLayout = QGridLayout()
        self.ResultsLogLayout.addWidget(self.ResultsLogLabel, 0, 0)
        self.ResultsLogLayout.addWidget(self.ResultsLogTextEdit, 1, 0)
        self.Layout.addLayout(self.ResultsLogLayout, 0, 1, 2, 1)

        # Set and Configure Layout
        self.Layout.setColumnStretch(1, 1)
        self.Frame = QFrame()
        self.Frame.setLayout(self.Layout)
        self.setCentralWidget(self.Frame)

        # Create Actions
        self.CreateActions()

        # Create Menu Bar
        self.CreateMenuBar()

        # Create Status Bar
        self.StatusBar = self.statusBar()

        # Center Window
        self.Center()

        # Create Keybindings
        self.CreateKeybindings()

    def CreateActions(self):
        self.NewAction = QAction("New")
        self.NewAction.triggered.connect(self.NewActionTriggered)

        self.OpenAction = QAction("Open")
        self.OpenAction.triggered.connect(self.OpenActionTriggered)

        self.SaveAction = QAction("Save")
        self.SaveAction.triggered.connect(self.SaveActionTriggered)

        self.SaveAsAction = QAction("Save As")
        self.SaveAsAction.triggered.connect(self.SaveAsActionTriggered)

        self.GzipModeAction = QAction("Gzip Mode (Smaller Files)")
        self.GzipModeAction.setCheckable(True)
        self.GzipModeAction.setChecked(self.GzipMode)
        self.GzipModeAction.triggered.connect(self.ToggleGzipMode)

        self.SetThemeAction = QAction("Set Theme")
        self.SetThemeAction.triggered.connect(self.SetTheme)

        self.QuitAction = QAction("Quit")
        self.QuitAction.triggered.connect(self.close)

        self.RollAction = QAction("Roll")
        self.RollAction.triggered.connect(self.Roll)

        self.RollPresetRollAction = QAction("Roll Preset")
        self.RollPresetRollAction.triggered.connect(self.RollPresetRoll)

        self.AverageRollAction = QAction("Average Roll")
        self.AverageRollAction.triggered.connect(self.AverageRoll)

        self.SetCurrentRollAsDefaultAction = QAction("Set Current Roll as Default")
        self.SetCurrentRollAsDefaultAction.triggered.connect(self.SetCurrentRollAsDefault)

        self.CreateDieClockAction = QAction("Create Die Clock")
        self.CreateDieClockAction.triggered.connect(self.CreateDieClock)

        self.AddLogEntryAction = QAction("Add Log Entry")
        self.AddLogEntryAction.triggered.connect(self.AddLogEntry)

        self.RemoveLastLogEntryAction = QAction("Remove Last Log Entry")
        self.RemoveLastLogEntryAction.triggered.connect(self.RemoveLastLogEntry)

        self.ClearLogAction = QAction("Clear Log")
        self.ClearLogAction.triggered.connect(self.ClearLog)

    def CreateMenuBar(self):
        self.MenuBar = self.menuBar()

        self.FileMenu = self.MenuBar.addMenu("File")
        self.FileMenu.addAction(self.NewAction)
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SaveAction)
        self.FileMenu.addAction(self.SaveAsAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.GzipModeAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SetThemeAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.QuitAction)

        self.RollerMenu = self.MenuBar.addMenu("Roller")
        self.RollerMenu.addAction(self.RollAction)
        self.RollerMenu.addAction(self.RollPresetRollAction)
        self.RollerMenu.addAction(self.AverageRollAction)
        self.RollerMenu.addAction(self.SetCurrentRollAsDefaultAction)
        self.RollerMenu.addAction(self.CreateDieClockAction)

        self.LogMenu = self.MenuBar.addMenu("Log")
        self.LogMenu.addAction(self.AddLogEntryAction)
        self.LogMenu.addAction(self.RemoveLastLogEntryAction)
        self.LogMenu.addAction(self.ClearLogAction)

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"
        self.DefaultKeybindings["RollAction"] = "Ctrl+R"
        self.DefaultKeybindings["RollPresetRollAction"] = "Ctrl+Shift+R"
        self.DefaultKeybindings["AverageRollAction"] = "Ctrl+Alt+R"

    def GetResourcePath(self, RelativeLocation):
        return self.AbsoluteDirectoryPath + "/" + RelativeLocation

    def LoadConfigs(self):
        # Default Roll
        DefaultRollFile = self.GetResourcePath("Configs/DefaultRoll.cfg")
        if os.path.isfile(DefaultRollFile):
            with open(DefaultRollFile, "r") as DefaultRollConfigFile:
                self.DefaultRollData = self.JSONSerializer.DeserializeDataFromJSONString(DefaultRollConfigFile.read())
        else:
            self.DefaultRollData = {}
            self.DefaultRollData["Dice Number"] = 1
            self.DefaultRollData["Die Type"] = 20
            self.DefaultRollData["Modifier"] = 0

        self.DiceNumberSpinBox.setValue(self.DefaultRollData["Dice Number"])
        self.DieTypeSpinBox.setValue(self.DefaultRollData["Die Type"])
        self.ModifierSpinBox.setValue(self.DefaultRollData["Modifier"])

        # Keybindings
        KeybindingsFile = self.GetResourcePath("Configs/Keybindings.cfg")
        if os.path.isfile(KeybindingsFile):
            with open(KeybindingsFile, "r") as ConfigFile:
                self.Keybindings = json.loads(ConfigFile.read())
        else:
            self.Keybindings = copy.deepcopy(self.DefaultKeybindings)
        for Action, Keybinding in self.DefaultKeybindings.items():
            if Action not in self.Keybindings:
                self.Keybindings[Action] = Keybinding
        InvalidBindings = []
        for Action in self.Keybindings.keys():
            if Action not in self.DefaultKeybindings:
                InvalidBindings.append(Action)
        for InvalidBinding in InvalidBindings:
            del self.Keybindings[InvalidBinding]
        for Action, Keybinding in self.Keybindings.items():
            getattr(self, Action).setShortcut(Keybinding)

    def SaveConfigs(self):
        if not os.path.isdir(self.GetResourcePath("Configs")):
            os.mkdir(self.GetResourcePath("Configs"))

        # Default Roll
        with open(self.GetResourcePath("Configs/DefaultRoll.cfg"), "w") as DefaultRollConfigFile:
            DefaultRollConfigFile.write(json.dumps(self.DefaultRollData))

        # Keybindings
        with open(self.GetResourcePath("Configs/Keybindings.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Theme
        with open(self.GetResourcePath("Configs/Theme.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Theme))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Roller Methods
    def Roll(self):
        DiceNumber = self.DiceNumberSpinBox.value()
        DieType = self.DieTypeSpinBox.value()
        Modifier = self.ModifierSpinBox.value()
        self.DiceRoller.RollDice(DiceNumber, DieType, Modifier)
        self.UpdateUnsavedChangesFlag(True)

    def AverageRoll(self):
        DiceNumber = self.DiceNumberSpinBox.value()
        DieType = self.DieTypeSpinBox.value()
        Modifier = self.ModifierSpinBox.value()
        AverageResult = self.DiceRoller.AverageRoll(DiceNumber, DieType, Modifier)
        AverageResultText = "The average result of " + str(DiceNumber) + "d" + str(DieType) + ("+" if Modifier >= 0 else "") + str(Modifier) + " is:\n\n" + str(AverageResult)
        self.DisplayMessageBox(AverageResultText)

    def AddPresetRoll(self):
        PresetRollIndex = self.DiceRoller.AddPresetRoll()
        self.UpdateDisplay()
        EditPresetRollDialogInst = EditPresetRollDialog(self, PresetRollIndex, AddMode=True)
        if EditPresetRollDialogInst.Cancelled:
            self.DiceRoller.DeleteLastPresetRoll()
            self.UpdateDisplay()
        else:
            self.UpdateUnsavedChangesFlag(True)
            self.PresetRollsTreeWidget.SelectIndex(PresetRollIndex)

    def DeletePresetRoll(self):
        CurrentSelection = self.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.DisplayMessageBox("Are you sure you want to delete this preset roll?  This cannot be undone.", Icon=QMessageBox.Question, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
                CurrentPresetRoll = CurrentSelection[0]
                CurrentPresetRollIndex = CurrentPresetRoll.Index
                self.DiceRoller.DeletePresetRoll(CurrentPresetRollIndex)
                self.UpdateUnsavedChangesFlag(True)
                PresetRollsLength = len(self.DiceRoller.PresetRolls)
                if PresetRollsLength > 0:
                    self.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex if CurrentPresetRollIndex < PresetRollsLength else PresetRollsLength - 1)

    def EditPresetRoll(self):
        CurrentSelection = self.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            EditPresetRollDialogInst = EditPresetRollDialog(self, CurrentPresetRollIndex)
            if EditPresetRollDialogInst.UnsavedChanges:
                self.UpdateUnsavedChangesFlag(True)
                self.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex)

    def CopyPresetRoll(self):
        CurrentSelection = self.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            NewPresetRollIndex = self.DiceRoller.CopyPresetRoll(CurrentPresetRollIndex)
            self.UpdateUnsavedChangesFlag(True)
            self.PresetRollsTreeWidget.SelectIndex(NewPresetRollIndex)

    def MovePresetRollUp(self):
        self.MovePresetRoll(-1)

    def MovePresetRollDown(self):
        self.MovePresetRoll(1)

    def MovePresetRoll(self, Delta):
        CurrentSelection = self.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            if self.DiceRoller.MovePresetRoll(CurrentPresetRollIndex, Delta):
                self.UpdateUnsavedChangesFlag(True)
                self.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex + Delta)

    def RollPresetRoll(self):
        CurrentSelection = self.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            self.DiceRoller.RollPresetRoll(CurrentPresetRollIndex)
            self.UpdateUnsavedChangesFlag(True)
            self.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex)

    def SetCurrentRollAsDefault(self):
        self.DefaultRollData["Dice Number"] = self.DiceNumberSpinBox.value()
        self.DefaultRollData["Die Type"] = self.DieTypeSpinBox.value()
        self.DefaultRollData["Modifier"] = self.ModifierSpinBox.value()

    def CreateDieClock(self):
        CreateDieClockDialogInst = CreateDieClockDialog(self)
        if CreateDieClockDialogInst.Submitted:
            DieClockPresetRollIndex = len(self.DiceRoller.PresetRolls)
            self.DiceRoller.CreateDieClock(CreateDieClockDialogInst.Name, CreateDieClockDialogInst.DieType, CreateDieClockDialogInst.ComplicationThreshold)
            self.UpdateUnsavedChangesFlag(True)
            self.PresetRollsTreeWidget.SelectIndex(DieClockPresetRollIndex)

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.DiceRoller):
            self.DiceRoller = DiceRoller()
        self.UpdateDisplay()

    def OpenActionTriggered(self):
        OpenData = self.Open(self.DiceRoller)
        if OpenData is not None:
            self.DiceRoller = OpenData
        self.UpdateDisplay()

    def SaveActionTriggered(self):
        self.Save(self.DiceRoller)
        self.UpdateDisplay()

    def SaveAsActionTriggered(self):
        self.Save(self.DiceRoller, SaveAs=True)
        self.UpdateDisplay()

    def ToggleGzipMode(self):
        self.GzipMode = not self.GzipMode

    def closeEvent(self, event):
        Close = True
        if self.UnsavedChanges:
            SavePrompt = self.DisplayMessageBox("Save unsaved changes before closing?", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
            if SavePrompt == QMessageBox.Yes:
                if not self.Save(self.DiceRoller):
                    Close = False
            elif SavePrompt == QMessageBox.No:
                pass
            elif SavePrompt == QMessageBox.Cancel:
                Close = False
        if not Close:
            event.ignore()
        else:
            self.SaveConfigs()
            event.accept()

    def UpdateUnsavedChangesFlag(self, UnsavedChanges):
        self.UnsavedChanges = UnsavedChanges
        self.UpdateDisplay()

    # Log Menu Action Methods
    def AddLogEntry(self):
        LogText, OK = QInputDialog.getText(self, "Add Log Entry", "Add text to log:")
        if OK:
            if LogText == "":
                self.DisplayMessageBox("Log entries cannot be blank.")
                return
            self.DiceRoller.AddLogEntry(LogText)
            self.UpdateUnsavedChangesFlag(True)

    def RemoveLastLogEntry(self):
        if self.DisplayMessageBox("Are you sure you want to remove the last log entry?  This cannot be undone.", Icon=QMessageBox.Question, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
            self.DiceRoller.RemoveLastLogEntry()
            self.UpdateUnsavedChangesFlag(True)

    def ClearLog(self):
        if self.DisplayMessageBox("Are you sure you want to clear the log?  This cannot be undone.", Icon=QMessageBox.Question, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
            self.DiceRoller.ClearLog()
            self.UpdateUnsavedChangesFlag(True)

    # Display Update Methods
    def UpdateDisplay(self):
        # Results Log Display
        ResultsLogString = self.DiceRoller.CreateLogText()
        self.ResultsLogTextEdit.setPlainText(ResultsLogString)

        # Fill Preset Rolls Tree Widget
        CurrentSelection = self.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSelectionIndex = CurrentSelection[0].Index
            self.PresetRollsTreeWidget.FillFromPresetRolls()
            self.PresetRollsTreeWidget.SelectIndex(CurrentSelectionIndex)
        else:
            self.PresetRollsTreeWidget.FillFromPresetRolls()

        # Update Window Title
        self.UpdateWindowTitle()

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + CurrentFileTitleSection + UnsavedChangesIndicator)

    def DisplayMessageBox(self, Message, Icon=QMessageBox.Information, Buttons=QMessageBox.Ok, Parent=None):
        MessageBox = QMessageBox(self if Parent is None else Parent)
        MessageBox.setWindowIcon(self.WindowIcon)
        MessageBox.setWindowTitle(self.ScriptName)
        MessageBox.setIcon(Icon)
        MessageBox.setText(Message)
        MessageBox.setStandardButtons(Buttons)
        return MessageBox.exec_()

    def FlashStatusBar(self, Status, Duration=2000):
        self.StatusBar.showMessage(Status)
        QtCore.QTimer.singleShot(Duration, self.StatusBar.clearMessage)

    # Window Management Methods
    def Center(self):
        FrameGeometryRectangle = self.frameGeometry()
        DesktopCenterPoint = QApplication.primaryScreen().availableGeometry().center()
        FrameGeometryRectangle.moveCenter(DesktopCenterPoint)
        self.move(FrameGeometryRectangle.topLeft())

    def CreateThemes(self):
        self.Themes = {}

        # Light
        self.Themes["Light"] = QPalette()
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.WindowText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Base, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Midlight, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Highlight, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.HighlightedText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.LinkVisited, QColor(255, 0, 255, 255))

        # Dark
        self.Themes["Dark"] = QPalette()
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.WindowText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Base, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Text, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ButtonText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Highlight, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.LinkVisited, QColor(127, 140, 141, 255))

    def LoadTheme(self):
        self.CreateThemes()
        ThemeFile = self.GetResourcePath("Configs/Theme.cfg")
        if os.path.isfile(ThemeFile):
            with open(ThemeFile, "r") as ConfigFile:
                self.Theme = json.loads(ConfigFile.read())
        else:
            self.Theme = "Light"
        self.AppInst.setStyle("Fusion")
        self.AppInst.setPalette(self.Themes[self.Theme])

    def SetTheme(self):
        Themes = list(self.Themes.keys())
        Themes.sort()
        CurrentThemeIndex = Themes.index(self.Theme)
        Theme, OK = QInputDialog.getItem(self, "Set Theme", "Set theme (requires restart to take effect):", Themes, current=CurrentThemeIndex, editable=False)
        if OK:
            self.Theme = Theme
            self.DisplayMessageBox("The new theme will be active after SnakeEyes is restarted.")
