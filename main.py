from variable import Variable
from word import Word
from label import Label
from equation import Equation
from labelarrangement import LabelArrangement
from formula import Formula
from wesolver import WESolver
from lengthconstraint import LengthConstraint

def main():

    # format for creating a string variable: variable = Variable(variableName)
    X = Variable("X")
    # format for adding new word as follows: wordName = Word([])
    word1 = Word([])
    # currently the user can only either add a char or a string variable to a word
    # format for adding a char/var to a word: wordName.append(char/var)
    word1.append("a")
    word1.append(X)
    word1.append("b")

    # format for adding length constraint as follows: lengthConstraint = LengthConstraint(operator, lhsList, rhsList)
    # the constraint is: operator (the sum of the lhsList, the sum of the rhsList)
    # len of variable X is X.len()
    lcX = LengthConstraint("==", [X.len()], [3])


    word2 = Word([])
    Y = Variable("Y")
    lcY = LengthConstraint("==", [X.len()], [6])
    word2.append(Y)
    word2.append("b")

    word3 = Word([])
    word3.append(Y)
    word3.append(Variable("K"))

    word4 = Word([])
    word4.append(Variable("L"))

    # format for creating an equation: equationName = Equation(word1, word2)
    e1 = Equation(word1, word2)
    e2 = Equation(word3, word4)

    # format for creating a formula solver: solver = WESolver()
    weSolver = WESolver()
    # format for adding an equation: solver.appendEq(equation)
    weSolver.appendEq(e1)
    weSolver.appendEq(e2)
    # format for adding an length constraint: solver.appendLenConstraint(lengthConstraint)
    weSolver.appendLenConstraint(lcX)
    weSolver.appendLenConstraint(lcY)

    # solver.solve() solves the formula
    # solver.printStr() prints the solver result
    weSolver.solve()
    print(weSolver.printStr())

if __name__ == '__main__':
    main()