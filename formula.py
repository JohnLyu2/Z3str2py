from variable import Variable
from equation import Equation
from lensolver import LenSolver
from lengthconstraint import LengthConstraint

SAT = "SAT"
UNKNOWN = "Unknown"
UNSAT = "UNSAT"

class Formula:

    def __init__(self):
        self.equations = None
        self.lenConstraints = None
        self.ogArr = [] # original arrangements for all words
        self.mergeResult = [] # results from Merge on all equations; a list of arrangements for each equation
        self.mergeIndexBank = None # change to none later
        self.varIndexBank = None # change to none later
        self.mergePick = None # current pick of arrangement for each equation from self.mergeResult
        self.varProjFromMerge = None # every variable: variable projections from self.mergePick
        self.varList = None # helper for createAllVarIndexTuples(); think about whether need to clean it later
        self.varCounter = dict()
        self.charCounter = dict()
        self.varMapBank = None
        self.varMapPick = None
        self.varSplitLenList = None
        self.varSplitDict = None
        self.rwArrgmt = None
        self.rwWord = None
        self.splittedEq = None
        self.overlap = False

    def inputEqArray(self, eqList):
        self.equations = eqList

    def inputLenArray(self, lenList):
        self.lenConstraints = lenList

    def generateOgArr(self):
        for equation in self.equations:
            arrTuple = equation.generateOgArr(self.varCounter, self.charCounter)
            self.ogArr.append(arrTuple)

    def implyLenFromEqs(self):
        for equation in self.equations:
            implyLC = equation.impliedLenConstraint()
            self.lenConstraints.append(implyLC)

    def solveLenConstraint(self):
        lenSolver = LenSolver(self.lenConstraints)
        return lenSolver.solve()

    # returns: (1) whether has 1 or more arr for every variable; (2) overlap occurs in the process; (3) must be UNSAT
    def intialMerge(self):
        isInvalid = False  # no solution can exist because for a certain variable
        noNonOverSol = False  # no solution without overlap
        hasOverlap = False
        for eqt in self.equations:
            eqMergeList, containOverlap = eqt.merge()
            if (len(eqMergeList) == 0):
                noNonOverSol = True
                if not containOverlap: isInvalid = True
            if containOverlap: hasOverlap = True
            self.mergeResult.append(eqMergeList)
        return (not noNonOverSol), hasOverlap, isInvalid

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
        #printList = []
        #for arrgmt in self.mergePick:
        #    printList.append(arrgmt.printStr())
        #print("Merge Pick List: ")
        #print(printList)

    # may rename some variable to variableName to eliminate ambiguity
    def selectFromVar(self, indexTuple):
        self.varMapPick = dict()
        for i in range(len(indexTuple)):
            variable = self.varList[i]
            index = indexTuple[i]
            self.varMapPick[variable] = self.varMapBank[variable][index]

    def varSplit(self):
        self.varSplitDict = dict()
        self.varSplitLenList = []
        for var in self.varList:
            varArr = self.varMapPick[var]
            varArrSize = varArr.getSetSize()
            if varArrSize > 2:
                spVarList = []
                spVarLenList = []
                for n in range(1, varArrSize):
                    newVarName = var.name + "_" + str(n)
                    newVar = Variable(newVarName)
                    newVarLC = LengthConstraint(">", [newVar.len()], [0])
                    self.varSplitLenList.append(newVarLC)
                    var.addChild(newVar)
                    print("add " + newVar.name + " to " + var.name)
                    spVarList.append(newVar)
                    spVarLenList.append(newVar.len())
                self.varSplitDict[var] = spVarList
                spLC = LengthConstraint("==", spVarLenList, [var.len()])
                self.varSplitLenList.append(spLC)
            else:
                self.varSplitDict[var] = [var]

    def solveFromVarPick(self):
        self.varSplit()
        self.rewrite()
        self.splitEq()
        splitFormula = Formula()
        splitFormula.inputEqArray(self.splittedEq)
        inputLCList = self.lenConstraints + self.varSplitLenList
        splitFormula.inputLenArray(inputLCList)
        print("Now Split New Formula to: ")
        print(splitFormula.printStr())
        return splitFormula.solve()

    def clearVarChildren(self):
        for var in self.varCounter:
            print("clear for " + var.name)
            var.children = []

    # def solveIterativeSelectFromVar(self):
        # containOverlap = False
        # for indexTuple in self.varIndexBank:
            # self.clearVarChildren()
            # self.selectFromVar(indexTuple)
            # solveResult = self.solveFromVarPick()
            # if solveResult == SAT: return SAT
            # elif solveResult == UNKNOWN:
                # containOverlap = True
        # if containOverlap: return UNKNOWN
        # return UNSAT

    def solveFromMergePick(self):
        self.varPjFromMerge()
        hasOverlap = False
        continuableBank, overlap, isInvalid = self.genVarMapBank()
        if isInvalid: return UNSAT
        if overlap: hasOverlap = True
        if continuableBank:
            self.createAllVarIndexTuples()
            for indexTuple in self.varIndexBank:
                self.clearVarChildren()
                self.selectFromVar(indexTuple)
                print("now solve from Var: " + str(indexTuple))
                solveResult = self.solveFromVarPick()
                if solveResult == SAT: return SAT
                elif solveResult == UNKNOWN: hasOverlap = True

        if hasOverlap: return UNKNOWN
        return UNSAT

    def solveIterativeSelectFromMerge(self):
        hasOverlap = False
        for indexTuple in self.mergeIndexBank:
            self.selectFromMerge(indexTuple)
            print("now solve from Merge: " + str(indexTuple))
            solveResult = self.solveFromMergePick()
            if solveResult == SAT: return SAT
            elif solveResult == UNKNOWN: hasOverlap = True
        if hasOverlap: return UNKNOWN
        return UNSAT

    def varPjFromMerge(self):
        self.varProjFromMerge = dict()
        for variable in self.varCounter:
            pjList = []
            for arrgmt in self.mergePick:
                pjList += arrgmt.projectArrgmtToVar(variable)
            self.varProjFromMerge[variable] = pjList

    # returns the merge result of var's projections
    def perVarArr(self, var):
        overlap = False
        pjList = self.varProjFromMerge[var]
        result = [pjList[0]]
        for i in range(1,len(pjList)):
            result, hasOverlap = pjList[i].arrMergeList(result)
            if hasOverlap: overlap = True
        return result, overlap

    # returns: (1) whether has 1 or more arr for every variable; (2) overlap occurs in the process; (3) must be UNSAT
    def genVarMapBank(self):
        hasOverlap = False
        isInvalid = False # no solution can exist because for a certain variable
        noNonOverSol = False # no solution without overlap
        self.varMapBank = dict()
        for variable in self.varCounter:
            varArrList, containOverlap = self.perVarArr(variable)
            if containOverlap: hasOverlap = True
            if len(varArrList) == 0:
                noNonOverSol = True
                if not containOverlap: isInvalid = True
            self.varMapBank[variable] = varArrList
        self.varList = list(self.varMapBank)
        return (not noNonOverSol), hasOverlap, isInvalid

    def rewrite(self):
        self.rwArrgmt = []
        self.rwWord = []
        for eqt in self.equations:
            lhsRwTuple = eqt.lhs.rewriteWD(eqt.lhsArr, self.varMapPick, self.varSplitDict)
            lhsRwArr = lhsRwTuple[0]
            lhsRwWord = lhsRwTuple[1]
            rhsRwTuple = eqt.rhs.rewriteWD(eqt.rhsArr, self.varMapPick, self.varSplitDict)
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
        assert (lhsEndMark == (lhsArrSize - 1))
        assert(rhsEndMark == (rhsArrSize - 1))

    def splitEq(self):
        self.splittedEq = []
        for i in range(len(self.equations)):
            # print("split eq: " + str(i))
            self.splitEqPos(i)

    # a recursive helper function for assignModel(self)
    def assignModelToFormula(self, eqList):
        unSolvedList = []
        eqSolved = 0
        for eqt in eqList:
            if eqt.assignDefModel(): eqSolved += 1
            else: unSolvedList.append(eqt)
        if len(unSolvedList) != 0:
            if eqSolved == 0:
                eqList[0].lhs.content[0].assignLenStr()
            self.assignModelToFormula(unSolvedList)

    def assignModel(self):
        lcSolver = LenSolver(self.lenConstraints)
        lcSolver.solve()
        mdl = lcSolver.model
        print(mdl)
        for var in self.varCounter:
            var.updateLengthFromModel(mdl)
        self.assignModelToFormula(self.equations)

    def isSolvable(self):
        for eqt in self.equations:
            if not eqt.isSolvable(): return False
        self.assignModel()
        return True

    # the flow of deciding UNKNOWN and UNSAT need more tests
    def solve(self):
        self.implyLenFromEqs()
        self.generateOgArr()
        if not self.solveLenConstraint():
            print(self.printStr())
            print("length constraints are UNSAT")
            for lc in self.lenConstraints:
                print(lc.printStr())
            return UNSAT
        if self.isSolvable():
            print("The format is solvable in the form: ")
            print(self.printStr())
            return SAT
        continuable, hasOverlap, isInvalid = self.intialMerge()
        if isInvalid: return UNSAT
        if not continuable: return UNKNOWN
        if hasOverlap: self.overlap = True
        self.createAllArrIndexTuples()
        solveResult = self.solveIterativeSelectFromMerge()
        if solveResult == SAT: return SAT
        if solveResult == UNKNOWN: return UNKNOWN
        if self.overlap: return UNKNOWN
        return UNSAT

    def printStr(self):
        resultStr = "{\n"
        for eq in self.equations:
            resultStr += "  "
            resultStr += eq.printStr()
            resultStr += "\n"
        resultStr += "}"
        return resultStr

