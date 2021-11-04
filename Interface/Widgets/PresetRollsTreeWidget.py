from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class PresetRollsTreeWidget(QTreeWidget):
    def __init__(self, MainWindow):
        super().__init__()

        # Store Parameters
        self.MainWindow = MainWindow

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def FillFromPresetRolls(self):
        self.clear()
        for PresetRollIndex in range(len(self.MainWindow.DiceRoller.PresetRolls)):
            self.invisibleRootItem().addChild(PresetRollsWidgetItem(PresetRollIndex, self.MainWindow.DiceRoller.PresetRolls[PresetRollIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class PresetRollsWidgetItem(QTreeWidgetItem):
    def __init__(self, Index, PresetRoll):
        super().__init__()

        # Store Parameters
        self.Index = Index
        self.PresetRoll = PresetRoll

        # Set Text
        self.setText(0, self.PresetRoll["Name"])
        self.setToolTip(0, self.PresetRoll["Name"])
