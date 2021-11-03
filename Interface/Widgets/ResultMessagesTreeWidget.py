from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class ResultMessagesTreeWidget(QTreeWidget):
    def __init__(self, EditPresetRollDialogInst):
        super().__init__()

        # Store Parameters
        self.EditPresetRollDialogInst = EditPresetRollDialogInst

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def FillFromResultMessages(self):
        self.clear()
        for ResultMessage in self.EditPresetRollDialogInst.PresetRoll["Result Messages"]:
            self.invisibleRootItem().addChild(ResultMessagesWidgetItem(ResultMessage))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)


class ResultMessagesWidgetItem(QTreeWidgetItem):
    def __init__(self, ResultMessage):
        super().__init__()

        # Store Parameters
        self.ResultMessage = ResultMessage

        # Determine Item Text
        ItemText = ""
        if ResultMessage["Result Min"] == ResultMessage["Result Max"]:
            ItemText += str(ResultMessage["Result Min"]) + ":  "
        else:
            ItemText += str(ResultMessage["Result Min"]) + "-" + str(ResultMessage["Result Max"]) + ":  "
        ItemText += ResultMessage["Result Text"]

        # Set Text
        self.setText(0, ItemText)
