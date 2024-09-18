from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class ResultMessagesTreeWidget(QTreeWidget):
    def __init__(self, EditPresetRollDialogInst):
        super().__init__()

        # Store Parameters
        self.EditPresetRollDialogInst = EditPresetRollDialogInst

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def FillFromResultMessages(self):
        self.clear()
        for ResultMessageIndex in range(len(self.EditPresetRollDialogInst.PresetRoll["Result Messages"])):
            self.invisibleRootItem().addChild(ResultMessagesWidgetItem(ResultMessageIndex, self.EditPresetRollDialogInst.PresetRoll["Result Messages"][ResultMessageIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class ResultMessagesWidgetItem(QTreeWidgetItem):
    def __init__(self, Index, ResultMessage):
        super().__init__()

        # Store Parameters
        self.Index = Index
        self.ResultMessage = ResultMessage

        # Determine Item Text
        ItemText = ""
        if ResultMessage["Result Min"] == ResultMessage["Result Max"]:
            ItemText += f"{str(ResultMessage["Result Min"])}:  "
        else:
            ItemText += f"{str(ResultMessage["Result Min"])}-{str(ResultMessage["Result Max"])}:  "
        ItemText += ResultMessage["Result Text"]

        # Set Text
        self.setText(0, ItemText)
        self.setToolTip(0, ItemText)
