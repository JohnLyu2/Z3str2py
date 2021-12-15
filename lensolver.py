from z3 import *

class LenSolver:

    def __init__(self, lenList):
        self.lenLst = lenList
        self.solver = None
        self.slvResult = None
        self.model = None

    # def addLenConstraint(self, lenConstraint):
        # self.lenLst.append(lenConstraint)

    def addLenConToSolver(self, lenConstraint):
        lhsList = lenConstraint.lhsList
        rhsList = lenConstraint.rhsList
        operator = lenConstraint.operator
        sumLeft = sum(lhsList)
        sumRight = sum(rhsList)
        if operator == "==":
            self.solver.add(sumLeft == sumRight)
        if operator == ">":
            self.solver.add(sumLeft > sumRight)
        if operator == ">=":
            self.solver.add(sumLeft >= sumRight)
        if operator == "<":
            self.solver.add(sumLeft < sumRight)
        if operator == "<=":
            self.solver.add(sumLeft <= sumRight)

    def solve(self):
        self.solver = Solver()
        for lenConstraint in self.lenLst:
            self.addLenConToSolver(lenConstraint)
        self.slvResult = (self.solver.check() == sat)
        if self.slvResult:
            self.model = self.solver.model()
        return self.slvResult

