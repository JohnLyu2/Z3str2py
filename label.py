class Label:

    def __init__(self, isVar, name, isStart, occ = 0):
        self.isVar = isVar
        # variable name for variable; char content for char
        self.name = name
        self.isStart = isStart
        self.occurance = occ

    def printStr(self):
        varStr = "char"
        if self.isVar:
            varStr = "var"
        posStr = "end"
        if self.isStart:
            posStr = "start"
        occStr = " (" + str(self.occurance) + ")"
        return "(" + self.name + occStr + "; " + varStr + "; " + posStr + ")"