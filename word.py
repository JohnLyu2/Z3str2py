from variable import Variable
from label import Label
from labelarrangement import LabelArrangement

class Word:

    def __init__(self, list):
        self.content = list

    def getSize(self):
        return len(self.content)

    def append(self, element):
        # add condition checker
        self.content.append(element)

    # return a subword from self, from start to end (not including end)
    def subWord(self, start, end):
        subList = self.content[start:end]
        return Word(subList)

    # this function updates the variable counter in Formula
    def createLabel(self, pos, isStart, varCounter, charCounter):
        element = self.content[pos]
        name = element
        counter = charCounter
        isVar = False
        if not type(element) is str:
            isVar = True
            counter = varCounter
            name = element.getName()
        if isStart:
            if name not in counter:
                counter[name] = 1
            else:
                counter[name] += 1
        occ = counter[name]
        label = Label(isVar, name, isStart, occ)
        return label

    # word has at least one element
    def getArrgmtFromWord(self, varCounter, charCounter):
        size = len(self.content)
        arrgmt = LabelArrangement([])
        label1 = self.createLabel(0, True, varCounter, charCounter)
        set1 = {label1}
        arrgmt.append(set1)
        for i in range(1, size):
            label_before = self.createLabel(i - 1, False, varCounter, charCounter)
            label_after = self.createLabel(i, True, varCounter, charCounter)
            labset = {label_before, label_after}
            arrgmt.append(labset)
        label_last = self.createLabel(size - 1, False, varCounter, charCounter)
        set_last = {label_last}
        arrgmt.append(set_last)
        return arrgmt



    def rewriteWD(self, ogArr, varArrMap):
        size = self.getSize()
        emptySet = set()
        arrResult = LabelArrangement([emptySet])
        wordList = []
        for i in range(size):
            leftLabArr = ogArr.trimArrgmt(i, i)
            rightLabArr = ogArr.trimArrgmt(i + 1, i + 1)
            eleArr = leftLabArr.appendArrgmt(rightLabArr)
            insertEle = self.content[i]
            if not type(insertEle) is str:
                varName = insertEle.getName()
                varArr = varArrMap[varName]
                eleArr = leftLabArr.mergeConcat(varArr)
                eleArr = eleArr.mergeConcat(rightLabArr)
                varArrSize = varArr.getSetSize()
                assert varArrSize > 1
                if varArrSize > 2:
                    for n in range(1, varArrSize):
                        newVarName = varName + "_" + str(n)
                        newVar = Variable(newVarName)
                        insertEle.addChild(newVar)
                        wordList.append(newVar)
                else:
                    wordList.append(insertEle) # for non-split variable
            else:
                wordList.append(insertEle) # for char
            arrResult = arrResult.mergeConcat(eleArr)
            wordResult = Word(wordList)
        return arrResult, wordResult

    def printStr(self):
        resultStr = ""
        for element in self.content:
            if type(element) is str:
                addStr = "\"" + element + "\" "
                resultStr += addStr
            else:
                addStr = element.printStr() + " "
                resultStr += addStr
        return resultStr

