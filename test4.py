from variable import Variable
from word import Word
from label import Label
from equation import Equation
from labelarrangement import LabelArrangement
from formula import Formula

def main():

    # format for adding new word as follows: wordName = Word([])
    word1 = Word([])
    word1.append("a")
    word1.append(Variable("X"))
    word1.append("b")

    word2 = Word([])
    word2.append(Variable("Y"))
    word2.append("b")

    word3 = Word([])
    word3.append(Variable("Y"))
    word3.append(Variable("K"))

    word4 = Word([])
    word4.append(Variable("L"))
    # word4.append(Variable("X"))


    e1 = Equation(word1, word2)
    e2 = Equation(word3, word4)

    fm = Formula()
    fm.appendEq(e1)
    fm.appendEq(e2)

    print(fm.solve())


    '''
    word3 = Word()
    word3.append(Variable("Z"))
    word3.append("a")
    word3.append(Variable("Y"))

    word4 = Word()
    word4.append(Variable("X"))
    word4.append("c")
    word4.append(Variable("X"))
    # word4.append(Variable("X"))

    e2 = Equation(word3, word4)

    fm2 = Formula()
    fm2.appendEq(e2)

    arrList2 = fm2.generateEqArr()

    for eqArr in arrList2:
        print("total arr #: " + str(len(eqArr)))
        for arr in eqArr:
            print(arr.printStr())
            print(arr.checkConsistency())
            prjList = arr.projectArrgmtToVar("X")
            print("projection list for X: ")
            for parr in prjList:
                print(parr.printStr())
            print("\n")
    '''

if __name__ == '__main__':
    main()