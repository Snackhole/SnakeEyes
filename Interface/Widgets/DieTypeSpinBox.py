from PyQt5.QtWidgets import QSpinBox


class DieTypeSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.StepValues = [4, 6, 8, 10, 12, 20, 100]

    def stepBy(self, StepDelta):
        CurrentValue = self.value()
        TargetValue = None
        if StepDelta == 1:
            for StepValue in self.StepValues:
                if CurrentValue < StepValue:
                    TargetValue = StepValue
                    break
        elif StepDelta == -1:
            for StepValue in reversed(self.StepValues):
                if CurrentValue > StepValue:
                    TargetValue = StepValue
                    break
        if TargetValue is not None:
            self.setValue(TargetValue)
            self.selectAll()
        else:
            super().stepBy(StepDelta)
