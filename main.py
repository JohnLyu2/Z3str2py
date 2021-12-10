from variable import Variable
from word import Word
from label import Label
from equation import Equation
from labelarrangement import LabelArrangement
from formula import Formula
from wesolver import WESolver

# fix instruction regarding variable later
def main():

    # format for adding new word as follows: wordName = Word([])
    word1 = Word([])
    # currently the user can only either add a char or a string variable to a word
    # format for adding a char to a word: wordName.append(char)
    word1.append("a")
    # a string variable is created as: Variable(variableName)
    # format for adding a string variable to a word: wordName.append(stringVariable)
    X = Variable("X")
    word1.append(X)
    word1.append("b")

    word2 = Word([])
    Y = Variable("Y")
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

    # format for creating a formula: formulaName = Formula()
    weSolver = WESolver()
    # format for adding an equation: formula.appendEq(equation)
    weSolver.appendEq(e1)
    weSolver.appendEq(e2)

    # formula.solve() returns True if it is solvable; returns False if not
    # Currently formula.solve() automatically print the final solvable split equations if the formula is solvable
    weSolver.solve()
    print(weSolver.printStr())

if __name__ == '__main__':
    main()