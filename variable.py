from z3 import *

class Variable:

    def __init__(self, name):
        self.name = name
        self.content = None
        self.children = []
        self.length = None
        self.assigned = False
        self.lenVar = Int(name)

    def getName(self):
        return self.name

    def len(self):
        return self.lenVar

    def printStr(self):
        return "<" + self.name + ">"

    def addChild(self, child):
        self.children.append(child)

    def updateLengthFromModel(self, mdl):
        # print("update length for var: " + self.name + " to " + str(mdl[self.lenVar]))
        self.length = mdl[self.lenVar].as_long()

    def assignStr(self, str):
        self.content = str
        self.assigned = True

    # assign this variable with a string of self.length
    def assignLenStr(self):
        # print("assign to: " + self.name)
        character = "0"
        str = ""
        for i in range(self.length):
            str += character
        self.content = str
        self.assigned = True

    def genModel(self):
        print("generate model str for: " + self.name)
        if len(self.children) == 0:
            print("no child")
            return self.content
        resultStr = ""
        for subVar in self.children:
            print(subVar.name)
            resultStr += subVar.genModel()
        self.content = resultStr
        return resultStr

    def modelPrintStr(self):
        printStr = "Variable " + self.name + ": \"" + self.content + "\""
        return printStr