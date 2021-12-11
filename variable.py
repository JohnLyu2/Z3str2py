class Variable:

    def __init__(self, name):
        self.name = name
        self.content = None
        self.children = []
        self.lenConstraint = 1 # default to be 1
        self.assigned = False

    def getName(self):
        return self.name

    def printStr(self):
        return "<" + self.name + ">"

    def addChild(self, child):
        self.children.append(child)

    def assignStr(self, str):
        self.content = str
        self.assigned = True

    # assign this variable with a string of length (self.lenConstraint)
    def assignLenStr(self):
        character = "0"
        str = ""
        for i in range(self.lenConstraint):
            str += character
        self.content = str
        self.assigned = True

    def genModel(self):
        if len(self.children) == 0: return self.content
        resultStr = ""
        for subVar in self.children:
            resultStr += subVar.genModel()
        self.content = resultStr
        return resultStr

    def modelPrintStr(self):
        printStr = "Variable " + self.name + ": " + self.content
        return printStr