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

    def assignModel(self):
        assert self.isSolvable()
        # it would not happen that char = char, and the characters are not the same after merge
        lhsEle = self.lhs.content[0]
        rhsEle = self.rhs.content[0]
        if (type(lhsEle) is str) and (not (type(rhsEle) is str)):
            rhsEle.assignAChar(lhsEle)
        elif (type(rhsEle) is str) and (not (type(lhsEle) is str)):
            lhsEle.assignAChar(rhsEle)
        elif (not (type(rhsEle) is str)) and (not (type(lhsEle) is str)):
            assert lhsEle.lenConstraint == rhsEle.lenConstraint
            # for now, we use the same character for stuffing; thus, it is ok just let the variables assign independently
            lhsEle.assignLenStr()
            rhsEle.assignLenStr()

    def printStr(self):
        resultStr = self.lhs.printStr()
        midStr = " = "
        resultStr += midStr
        resultStr += self.rhs.printStr()
        return resultStr