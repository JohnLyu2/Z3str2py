from equation import Equation

class Formula:

    def __init__(self):
        self.equations = []
        self.ogArr = [] # orignal arrangments for all words
        self.mergeResult = [] # results from Merge on all equations; a list of arrangements for each equation
        self.mergeIndexBank = None # change to none later
        self.varIndexBank = None # change to none later
        self.mergePick = None # current pick of arrangement for each equation from self.mergeResult
        self.varProjFromMerge = None # every variable: variable projections from self.mergePick
        self.varList = None # helper for createAllVarIndexTuples()
        self.varCounter = dict()
        self.charCounter = dict()
        self.varMapBank = None
        self.varMapPick = None
        self.rwArrgmt = None
        self.rwWord = None
        self.splittedEq = None

    def inputEqArray(self, eqList):
        self.equations = eqList

    def appendEq(self, equation):
        self.equations.append(equation)

    def generateOgArr(self):
        for equation in self.equations:
            arrTuple = equation.generateOgArr(self.varCounter, self.charCounter)
            self.ogArr.append(arrTuple)

    def intialMerge(self):
        for eqt in self.equations:
            eqMergeList = eqt.merge()
            if (len(eqMergeList) == 0): return False
            self.mergeResult.append(eqMergeList)
        return True

    def createAllArrIndexTuples(self):
        self.mergeIndexBank = []
        sizeList = []
        for arrList in self.mergeResult:
            sizeList.append(len(arrList))
        sizeList.append(0) # the last element is trivial
        eqNum = len(self.equations)
        recordList = []
        for i in range(eqNum+1): # one more in the size for check end of the subroutine
            recordList.append(0)
        p = 0
        while recordList[eqNum] == 0:
            insertTuple = tuple(recordList[:-1])
            # print(insertTuple) # debug info
            self.mergeIndexBank.append(insertTuple)
            recordList[0] = recordList[0] + 1
            while recordList[p] == sizeList[p]:
                recordList[p] = 0
                p += 1
                recordList[p] += 1
                if recordList[p] != sizeList[p]:
                    p = 0

    def createAllVarIndexTuples(self):
        self.varIndexBank = []
        sizeList = []
        for var in self.varList:
            sizeList.append(len(self.varMapBank[var]))
        sizeList.append(0)  # the last element is trivial
        varNum = len(self.varList)
        recordList = []
        for i in range(varNum + 1):  # one more in the size for check end of the subroutine
            recordList.append(0)
        p = 0
        while recordList[varNum] == 0:
            insertTuple = tuple(recordList[:-1])
            # print(insertTuple)  # debug info
            self.varIndexBank.append(insertTuple)
            recordList[0] = recordList[0] + 1
            while recordList[p] == sizeList[p]:
                recordList[p] = 0
                p += 1
                recordList[p] += 1
                if recordList[p] != sizeList[p]:
                    p = 0

    # Select current arrangement from self.mergeResult according to indexTuple
    def selectFromMerge(self, indexTuple):
        # print("Select From " + str(indexTuple))
        self.mergePick = []
        eqNum = len(self.equations)
        for i in range(eqNum):
            arrList = self.mergeResult[i]
            index = indexTuple[i]
            self.mergePick.append(arrList[index])

    def selectFromVar(self, indexTuple):
        self.varMapPick = dict()
        for i in range(len(indexTuple)):
            variable = self.varList[i]
            index = indexTuple[i]
            self.varMapPick[variable] = self.varMapBank[variable][index]

    def solveFromVarPick(self):
        self.rewrite()
        self.splitEq()
        splitFormula = Formula()
        splitFormula.inputEqArray(self.splittedEq)
        # print("Now Split New Formula to: ")
        # print(splitFormula.printStr())
        return splitFormula.solve()

    def solveIterativeSelectFromVar(self):
        # think about empty bank case later together
        for indexTuple in self.varIndexBank:
            self.selectFromVar(indexTuple)
            if self.solveFromVarPick(): return True
        else:
            return False

    def solveFromMergePick(self):
        self.varPjFromMerge()
        if not self.genVarMapBank(): return False
        self.createAllVarIndexTuples()
        for indexTuple in self.varIndexBank:
            self.selectFromVar(indexTuple)
            # print("now solve from Var: " + str(indexTuple))
            if self.solveFromVarPick(): return True
        else: return False

    def solveIterativeSelectFromMerge(self):
        # think about empty bank case later together
        for indexTuple in self.mergeIndexBank:
            self.selectFromMerge(indexTuple)
            # print("now solve from Merge: " + str(indexTuple))
            if self.solveFromMergePick(): return True
        else: return False

    def varPjFromMerge(self):
        self.varProjFromMerge = dict()
        for variable in self.varCounter:
            pjList = []
            for arrgmt in self.mergePick:
                pjList += arrgmt.projectArrgmtToVar(variable)
            self.varProjFromMerge[variable] = pjList

    # returns the merge result of var's projections
    def perVarArr(self, var):
        pjList = self.varProjFromMerge[var]
        result = [pjList[0]]
        for i in range(1,len(pjList)):
            result = pjList[i].arrMergeList(result)
        return result

    def genVarMapBank(self):
        self.varMapBank = dict()
        for variable in self.varCounter:
            varArrList = self.perVarArr(variable)
            if len(varArrList) == 0: return False
            self.varMapBank[variable] = varArrList
        self.varList = list(self.varMapBank)
        return True


    def rewrite(self):
        self.rwArrgmt = []
        self.rwWord = []
        for eqt in self.equations:
            lhsRwTuple = eqt.lhs.rewriteWD(eqt.lhsArr, self.varMapPick)
            lhsRwArr = lhsRwTuple[0]
            lhsRwWord = lhsRwTuple[1]
            rhsRwTuple = eqt.rhs.rewriteWD(eqt.rhsArr, self.varMapPick)
            rhsRwArr = rhsRwTuple[0]
            rhsRwWord = rhsRwTuple[1]
            self.rwArrgmt.append((lhsRwArr, rhsRwArr))
            self.rwWord.append((lhsRwWord, rhsRwWord))

    # returns (arrStart+1, posL, posR)
    # find the first (posL, posR) that for the equation[pos], lhsArr[posL] intersection with arr[arrStart+1]
    # rhsArr[posR] intersection with arr[arrStart+1] and posL > lhsStart and posR > rhsStart
    def findNonEmptyUnion(self, pos, arrStart, lhsStart, rhsStart):
        lhsArrSize = self.rwArrgmt[pos][0].getSetSize()
        rhsArrSize = self.rwArrgmt[pos][1].getSetSize()
        lhsArr = self.rwArrgmt[pos][0]
        rhsArr = self.rwArrgmt[pos][1]
        targetSet = self.mergePick[pos].getPosSet(arrStart+1)
        posL = -1
        posR = -1
        for i in range(lhsStart+1, lhsArrSize):
            lhsSet = lhsArr.getPosSet(i)
            if not lhsSet.isdisjoint(targetSet):
                posL = i
                break
        for i in range(rhsStart + 1, rhsArrSize):
            rhsSet = rhsArr.getPosSet(i)
            if not rhsSet.isdisjoint(targetSet):
                posR = i
                break
        return (arrStart+1, posL, posR)

    def addSplitEquation(self, pos, lhsStartArr, lhsEndArr, rhsStartArr, rhsEndArr):
        lhsWord = self.rwWord[pos][0]
        rhsWord = self.rwWord[pos][1]
        lhsSubWord = lhsWord.subWord(lhsStartArr, lhsEndArr)
        rhsSubWord = rhsWord.subWord(rhsStartArr, rhsEndArr)
        splitEq = Equation(lhsSubWord, rhsSubWord)
        self.splittedEq.append(splitEq)

    # split the equation at pos
    def splitEqPos(self, pos):
        arrSize = self.mergePick[pos].getSetSize()
        # print("arrgmt: " + self.mergePick[pos].printStr())
        lhsArrSize = self.rwArrgmt[pos][0].getSetSize()
        # print("lhs re arr: " + self.rwArrgmt[pos][0].printStr())
        rhsArrSize = self.rwArrgmt[pos][1].getSetSize()
        # print("rhs re arr: " + self.rwArrgmt[pos][1].printStr())
        arrStartMark = 0
        lhsStartMark = 0
        rhsStartMark = 0
        lhsEndMark = -1
        rhsEndMark = -1
        arrEndMark = -1
        while (arrEndMark != (arrSize-1)):
            arrEndMark, lhsEndMark, rhsEndMark = self.findNonEmptyUnion(pos, arrStartMark, lhsStartMark, rhsStartMark)
            # print("lhs end mark: " + str(lhsEndMark))
            self.addSplitEquation(pos, lhsStartMark, lhsEndMark, rhsStartMark, rhsEndMark)
            arrStartMark = arrEndMark
            lhsStartMark = lhsEndMark
            rhsStartMark = rhsEndMark
        assert(rhsEndMark == (rhsArrSize - 1))

    def splitEq(self):
        self.splittedEq = []
        for i in range(len(self.equations)):
            # print("split eq: " + str(i))
            self.splitEqPos(i)

    def isSolvable(self):
        for eqt in self.equations:
            if not eqt.isSolvable(): return False
        return True

    def solve(self):
        if self.isSolvable():
            print("The format is solvable in the form: ")
            print(self.printStr())
            return True
        self.generateOgArr()
        if not self.intialMerge():
            return False
        self.createAllArrIndexTuples()
        return self.solveIterativeSelectFromMerge()

    def printStr(self):
        resultStr = "{\n"
        for eq in self.equations:
            resultStr += "  "
            resultStr += eq.printStr()
            resultStr += "\n"
        resultStr += "}"
        return resultStr

