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

    # assign definite models
    def assignDefModel(self):
        assert self.isSolvable()
        # it would not happen that char = char, and the characters are not the same after merge
        lhsEle = self.lhs.content[0]
        rhsEle = self.rhs.content[0]
        if (type(lhsEle) is str) and (type(rhsEle) is str): return True
        if (type(lhsEle) is str) and (not (type(rhsEle) is str)):
            rhsEle.assignStr(lhsEle)
            return True
        elif (type(rhsEle) is str) and (not (type(lhsEle) is str)):
            lhsEle.assignStr(rhsEle)
            return True
        if lhsEle.assigned and rhsEle.assigned: return True
        if lhsEle.assigned:
            rhsEle.assignStr(lhsEle.content)
            return True
        if rhsEle.assigned:
            lhsEle.assignStr(rhsEle.content)
            return True

    def printStr(self):
        resultStr = self.lhs.printStr()
        midStr = " = "
        resultStr += midStr
        resultStr += self.rhs.printStr()
        return resultStr