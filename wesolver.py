from formula import Formula

class WESolver:

    def __init__(self):
        self.ogEqList = []
        self.varSet = None
        self.solveResult = None

    def appendEq(self, equation):
        self.ogEqList.append(equation)

    # a helper function for genVarSet
    def addVarFromWord(self, word):
        for element in word.content:
            if not type(element) is str:
                self.varSet.add(element)

    def genVarSet(self):
        self.varSet = set()
        for eq in self.ogEqList:
            lhsWord = eq.lhs
            rhsWord = eq.rhs
            self.addVarFromWord(lhsWord)
            self.addVarFromWord(rhsWord)

    def solve(self):
        self.genVarSet()
        fm = Formula()
        fm.inputEqArray(self.ogEqList)
        self.solveResult = fm.solve()

    def ogFormulaStr(self):
        resultStr = "{\n"
        for eq in self.ogEqList:
            resultStr += "  "
            resultStr += eq.printStr()
            resultStr += "\n"
        resultStr += "}"
        return resultStr

    def modelStr(self):
        resultStr = ""
        for var in self.varSet:
            var.genModel()
            resultStr += var.modelPrintStr()
            resultStr += "\n"
        return resultStr

    def printStr(self):
        resultStr = "The formula: \n"
        resultStr += self.ogFormulaStr()
        resultStr += "\nis "
        resultStr += self.solveResult
        if self.solveResult == "True":
            resultStr += "\nA model is \n"
            resultStr += self.modelStr()
        return resultStr
