class Equation:

    def __init__(self, LHS, RHS):
        self.lhs = LHS
        self.rhs = RHS
        self.lhsArr = None
        self.rhsArr = None

    def generateOgArr(self, varCounter, charCounter):
        self.lhsArr = self.lhs.getArrgmtFromWord(varCounter, charCounter)
        # print("LHS: " + self.lhsArr.printStr())
        self.rhsArr = self.rhs.getArrgmtFromWord(varCounter, charCounter)
        # print("RHS: " + self.rhsArr.printStr())
        return (self.lhsArr, self.rhsArr)

    def merge(self):
        return self.lhsArr.arrgmtMerge(self.rhsArr)

    def isSolvable(self):
        if (self.lhs.getSize() == 1) and (self.rhs.getSize() == 1):
            return True
        return False

    def printStr(self):
        resultStr = self.lhs.printStr()
        midStr = " = "
        resultStr += midStr
        resultStr += self.rhs.printStr()
        return resultStr