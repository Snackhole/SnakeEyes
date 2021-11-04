import copy
import random

from SaveAndLoad.JSONSerializer import SerializableMixin


class DiceRoller(SerializableMixin):
    def __init__(self):
        # Initialize SerializableMixin
        super().__init__()

        # Randomizer
        self.Randomizer = random.Random()

        # Preset Rolls
        self.PresetRolls = []
        self.PresetRollsDefaults = {}
        self.PresetRollsDefaults["Name"] = "New Preset Roll"
        self.PresetRollsDefaults["Dice Number"] = 1
        self.PresetRollsDefaults["Die Type"] = 20
        self.PresetRollsDefaults["Modifier"] = 0
        self.PresetRollsDefaults["Result Messages"] = []
        self.ResultMessageDefaults = {}
        self.ResultMessageDefaults["Result Min"] = 1
        self.ResultMessageDefaults["Result Max"] = 1
        self.ResultMessageDefaults["Result Text"] = "New Result Message"

        # Results Log
        self.ResultsLog = []

    # Rolling Methods
    def RollDice(self, DiceNumber=1, DieType=6, Modifier=0, ResultMessages=None, LogPrefix="", SkipLogging=False):
        if ResultMessages is None:
            ResultMessages = []

        # Results Dictionary
        Results = {}
        Results["Dice Number"] = DiceNumber
        Results["Die Type"] = DieType
        Results["Modifier"] = Modifier
        Results["Rolls"] = []
        Results["Total"] = 0
        Results["Log Prefix"] = LogPrefix
        Results["Log Suffix"] = ""

        # Roll
        for Roll in range(DiceNumber):
            CurrentRollResult = self.Randomizer.randint(1, DieType)
            Results["Rolls"].append(CurrentRollResult)

        # Total Roll Results
        Results["Total"] = sum(Results["Rolls"]) + Modifier

        # Logging
        if not SkipLogging:
            # Log Suffix
            for ResultMessage in ResultMessages:
                if Results["Total"] >= ResultMessage["Result Min"] and Results["Total"] <= ResultMessage["Result Max"]:
                    Results["Log Suffix"] += "\n" + ResultMessage["Result Text"]

            # Add to Log
            self.ResultsLog.append(self.CreateLogEntryText(Results))

        return Results

    def RollPresetRoll(self, PresetRollIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        Results = self.RollDice(PresetRoll["Dice Number"], PresetRoll["Die Type"], PresetRoll["Modifier"], PresetRoll["Result Messages"], LogPrefix=PresetRoll["Name"] + ":\n")
        return Results

    def AverageRoll(self, DiceNumber=1, DieType=6, Modifier=0, NumberRolls=100000):
        RollResults = []
        for Roll in range(NumberRolls):
            RollResults.append(self.RollDice(DiceNumber, DieType, Modifier, SkipLogging=True)["Total"])
        AverageResult = sum(RollResults) / len(RollResults)
        return AverageResult

    # Preset Roll Methods
    def CreatePresetRoll(self):
        PresetRoll = {}
        PresetRoll["Name"] = self.PresetRollsDefaults["Name"]
        PresetRoll["Dice Number"] = self.PresetRollsDefaults["Dice Number"]
        PresetRoll["Die Type"] = self.PresetRollsDefaults["Die Type"]
        PresetRoll["Modifier"] = self.PresetRollsDefaults["Modifier"]
        PresetRoll["Result Messages"] = self.PresetRollsDefaults["Result Messages"]
        return PresetRoll

    def AddPresetRoll(self):
        PresetRoll = self.CreatePresetRoll()
        self.PresetRolls.append(PresetRoll)
        PresetRollIndex = len(self.PresetRolls) - 1
        return PresetRollIndex

    def DeletePresetRoll(self, PresetRollIndex):
        del self.PresetRolls[PresetRollIndex]

    def DeleteLastPresetRoll(self):
        PresetRollIndex = len(self.PresetRolls) - 1
        self.DeletePresetRoll(PresetRollIndex)

    def CopyPresetRoll(self, PresetRollIndex):
        self.PresetRolls.append(copy.deepcopy(self.PresetRolls[PresetRollIndex]))
        NewPresetRollIndex = len(self.PresetRolls) - 1
        return NewPresetRollIndex

    def MovePresetRoll(self, PresetRollIndex, Delta):
        TargetIndex = PresetRollIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(self.PresetRolls):
            return False
        SwapTarget = self.PresetRolls[TargetIndex]
        self.PresetRolls[TargetIndex] = self.PresetRolls[PresetRollIndex]
        self.PresetRolls[PresetRollIndex] = SwapTarget
        return True

    # Result Message Methods
    def CreateResultMessage(self):
        ResultMessage = {}
        ResultMessage["Result Min"] = self.ResultMessageDefaults["Result Min"]
        ResultMessage["Result Max"] = self.ResultMessageDefaults["Result Max"]
        ResultMessage["Result Text"] = self.ResultMessageDefaults["Result Text"]
        return ResultMessage

    def AddResultMessage(self, PresetRollIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        ResultMessage = self.CreateResultMessage()
        PresetRoll["Result Messages"].append(ResultMessage)
        ResultMessageIndex = len(PresetRoll["Result Messages"]) - 1
        return ResultMessageIndex

    def DeleteResultMessage(self, PresetRollIndex, ResultMessageIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        del PresetRoll["Result Messages"][ResultMessageIndex]

    def DeleteLastResultMessage(self, PresetRollIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        ResultMessageIndex = len(PresetRoll["Result Messages"]) - 1
        self.DeleteResultMessage(PresetRollIndex, ResultMessageIndex)

    def CopyResultMessage(self, PresetRollIndex, ResultMessageIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        PresetRoll["Result Messages"].append(copy.deepcopy(PresetRoll["Result Messages"][ResultMessageIndex]))
        NewResultMessageIndex = len(PresetRoll["Result Messages"]) - 1
        return NewResultMessageIndex

    def MoveResultMessage(self, PresetRollIndex, ResultMessageIndex, Delta):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        TargetIndex = ResultMessageIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(PresetRoll["Result Messages"]):
            return False
        SwapTarget = PresetRoll["Result Messages"][TargetIndex]
        PresetRoll["Result Messages"][TargetIndex] = PresetRoll["Result Messages"][ResultMessageIndex]
        PresetRoll["Result Messages"][ResultMessageIndex] = SwapTarget
        return True

    # Log Methods
    def CreateLogEntryText(self, Results):
        ResultText = Results["Log Prefix"]
        ResultText += str(Results["Dice Number"]) + "d" + str(Results["Die Type"]) + ("+" if Results["Modifier"] >= 0 else "") + str(Results["Modifier"]) + " ->\n"
        ResultText += str(Results["Rolls"]) + ("+" if Results["Modifier"] >= 0 else "") + str(Results["Modifier"]) + " ->\n"
        ResultText += str(Results["Total"])
        ResultText += Results["Log Suffix"]
        return ResultText

    def CreateLogText(self):
        LogText = ""
        for Results in reversed(self.ResultsLog):
            LogText += Results
            if not Results is self.ResultsLog[0]:
                LogText += "\n\n---\n\n"
        return LogText

    def RemoveLastLogEntry(self):
        self.ResultsLog = self.ResultsLog[:-1]

    def ClearLog(self):
        self.ResultsLog.clear()

    # Serialization Methods
    def SetState(self, NewState):
        self.PresetRolls = NewState["PresetRolls"]
        self.PresetRollsDefaults = NewState["PresetRollsDefaults"]
        self.ResultMessageDefaults = NewState["ResultMessageDefaults"]
        self.ResultsLog = NewState["ResultsLog"]

    def GetState(self):
        State = {}
        State["PresetRolls"] = self.PresetRolls
        State["PresetRollsDefaults"] = self.PresetRollsDefaults
        State["ResultMessageDefaults"] = self.ResultMessageDefaults
        State["ResultsLog"] = self.ResultsLog
        return State

    @classmethod
    def CreateFromState(cls, State):
        NewDiceRoller = cls()
        NewDiceRoller.SetState(State)
        return NewDiceRoller
