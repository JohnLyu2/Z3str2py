class LengthConstraint:

    def __init__(self, op, lhs, rhs):
        self.operator = op
        self.lhsList = lhs
        self.rhsList = rhs

    def printStr(self):
        lhsStr = str(self.lhsList[0])
        for i in range(1, len(self.lhsList)):
            lhsStr += (" + " + str(self.lhsList[i]))
        rhsStr = str(self.rhsList[0])
        for i in range(1, len(self.rhsList)):
            rhsStr += (" + " + str(self.rhsList[i]))
        return lhsStr + " " + self.operator + " " + rhsStr
