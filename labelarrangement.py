class LabelArrangement:

    def __init__(self, setList):
        self.arrangement = setList

    def getSetSize(self):
        return len(self.arrangement)

    # get the label set from arrangement at pos
    def getPosSet(self, pos):
        return self.arrangement[pos]

    def append(self, lSet):
        self.arrangement.append(lSet)

    def appendArrgmt(self, arr2):
        #print(type(self.arrangement))
        #print(type(arr2.arrangement))
        concatList = self.arrangement + arr2.arrangement
        return LabelArrangement(concatList)

    # returns the arrangement that excluding the first and last set; the size of sets is guaranteed >= 2
    # may combine with trimArrgmt later
    def midArrgmt(self):
        midList = self.arrangement[1:-1]
        return LabelArrangement(midList)

    # may combine with trimArrgmt later
    def fstSetArr(self):
        fstSet = self.arrangement[0]
        return LabelArrangement([fstSet])

    # may combine with trimArrgmt later
    def exFirstArrgmt(self):
        exFirstList = self.arrangement[1:]
        return LabelArrangement(exFirstList)

    # trim the arrangement from position start to end (inclusive)
    def trimArrgmt(self, start, end):
        remainList = self.arrangement[start:end+1]
        return LabelArrangement(remainList)

    def concatAList(self, arrList, after = True):
        result = []
        #print(self.printStr())
        for arr in arrList:
            if after: result.append(self.appendArrgmt(arr))
            else: result.append(arr.appendArrgmt(self))
        return result

    def arrgmtProductRec(self, arr2):
        if (self.getSetSize() == 0) and (arr2.getSetSize() == 0):
            return [LabelArrangement([])]
        if (self.getSetSize() == 0):
            return [arr2]
        if (arr2.getSetSize() == 0):
            return [self]
        # print("self" + self.exFirstArrgmt().printStr())
        # print("arr2" + arr2.printStr())
        subList1 = self.exFirstArrgmt().arrgmtProductRec(arr2)
        resultList1 = self.fstSetArr().concatAList(subList1)
        subList2 = self.exFirstArrgmt().arrgmtProductRec(arr2.exFirstArrgmt())
        firstSet2 = self.arrangement[0].union(arr2.arrangement[0])
        firstArr2 = LabelArrangement([firstSet2])
        resultList2 = firstArr2.concatAList(subList2)
        subList3 = self.arrgmtProductRec(arr2.exFirstArrgmt())
        resultList3 = arr2.fstSetArr().concatAList(subList3)
        result = resultList1 + resultList2 + resultList3
        return result

    def arrgmtProduct(self, arr2):
        size1 = len(self.arrangement)
        size2 = len(arr2.arrangement)
        firstSetArr = LabelArrangement([self.arrangement[0].union(arr2.arrangement[0])])
        lastSetArr = LabelArrangement([self.arrangement[size1 - 1].union(arr2.arrangement[size2 - 1])])

        midList = self.midArrgmt().arrgmtProductRec(arr2.midArrgmt())

        result1 = firstSetArr.concatAList(midList)
        result = lastSetArr.concatAList(result1, False)
        return result

    # check at arrangement[pos] whether there exists element (occ)'s end label
    def checkEnd(self, name, isVariable, occ, pos):
        for element in self.arrangement[pos]:
            if (element.isVar == isVariable) and (element.name == name) and (element.occurance == occ) and (not element.isStart):
                return True
        return False

    # find element (occ)'s end label position starting from startPos; if not found, return -1
    def findEnd(self, name, isVariable, occ, startPos):
        for i in range(startPos, len(self.arrangement)):
            if self.checkEnd(name, isVariable, occ, i): return i
        return -1

    def checkNeighboring(self):
        size = self.getSetSize()
        for i in range(size-1):
            for element in self.arrangement[i]:
                if (not element.isVar) and element.isStart:
                    if not self.checkEnd(element.name, element.isVar, element.occurance, i+1):
                        return False
        return True

    def checkConsistency(self):
        for lSet in self.arrangement:
            startSet = set()
            endSet = set()
            for element in lSet:
                if not element.isVar:
                    if element.isStart: startSet.add(element.name)
                    else: endSet.add(element.name)
            if (len(startSet) > 1) or (len(endSet) > 1):
                return False
        return True

    def checkUniqueness(self):
        existSet = set()
        for lSet in self.arrangement:
            for element in lSet:
                if element in existSet:
                    return False
                existSet.add(element)
        return True

    # check whether there exists a variable start label with name varName between pos start and end (exclusive)
    def checkExistVarStartInBetween(self, varName, start, end):
        for i in range(start + 1, end):
            lSet = self.arrangement[i]
            for label in lSet:
                if (label.isVar) and (label.name == varName) and (label.isStart):
                    return True
        return False

    # Works for arrangement complying with Neighboring, Consistency, and Uniqueness
    def checkOverlapping(self):
        setSize = self.getSetSize();
        for i in range(setSize - 2):
            startSet = self.arrangement[i]
            for label in startSet:
                if (label.isVar):
                    endPos = self.findEnd(label.name, True, label.occurance, i)
                    if self.checkExistVarStartInBetween(label.name, i, endPos): return True
        return False

    def arrgmtMerge(self, arr2):
        productList = self.arrgmtProduct(arr2)
        result = []
        containOverlap = False
        for arr in productList:
            isOverlap = arr.checkOverlapping();
            if arr.checkNeighboring() and arr.checkConsistency() and arr.checkUniqueness():
                if isOverlap:
                #    print("Overlap!!!: ")
                #    print(arr.printStr())
                    containOverlap = True
                else:
                    result.append(arr)
        return result, containOverlap

    # merge self with each arrangement in arrList and returns a list of all resulting arrangements
    def arrMergeList(self, arrList):
        result = []
        containOverlap = False
        for arr in arrList:
            oneResult, isOverlap = self.arrgmtMerge(arr)
            if (isOverlap): containOverlap = True
            result += oneResult
        return result, containOverlap

    def projectArrgmtToVar(self, var):
        resultList = []
        for i in range(len(self.arrangement)):
            for element in self.arrangement[i]:
                if element.isVar and (element.name == var.name) and (element.isStart):
                    endPos = self.findEnd(var.name, True, element.occurance, i+1)
                    resultList.append(self.trimArrgmt(i, endPos))
        return resultList

    # concatentate self and arr2: the last set in self and the first set in arr2 is merged (unioned)
    def mergeConcat(self, arr2):
        size = self.getSetSize()
        mergedSet = self.arrangement[size - 1].union(arr2.arrangement[0])
        resultList = self.arrangement[:-1] + [mergedSet] + arr2.arrangement[1:]
        return LabelArrangement(resultList)

    def printStr(self):
        pStr = "["
        for set in self.arrangement:
            pStr += "{"
            for label in set:
                pStr += label.printStr()
                pStr += " "
            pStr += "} "
        pStr += "]"
        return pStr