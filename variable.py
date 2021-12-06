class Variable:

    def __init__(self, name):
        self.name = name
        self.content = None

    def getName(self):
        return self.name

    def printStr(self):
        return "<" + self.name + ">"