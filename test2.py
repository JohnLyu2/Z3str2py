from variable import Variable
from word import Word
from label import Label
from equation import Equation
from labelarrangement import LabelArrangement
from formula import Formula

def main():

    word1 = Word()
    word1.append(Variable("X"))
    # word1.append(Variable("M"))
    # word1.append("b")

    word2 = Word()
    word2.append(Variable("N"))
    word2.append(Variable("Y"))
    word2.append(Variable("X"))

    word3 = Word()
    word3.append(Variable("Y"))
    word3.append(Variable("K"))

    word4 = Word()
    word4.append(Variable("L"))
    # word4.append(Variable("X"))

    e1 = Equation(word1, word2)
    e2 = Equation(word3, word4)

    fm = Formula()
    fm.appendEq(e1)
    fm.appendEq(e2)

    fm.go()

    for eqArr in fm.mergeResult:
        print("total arr #: " + str(len(eqArr)))
        for arr in eqArr:
            print(arr.printStr())
            print(arr.checkNeighboring())

    print("\nPick: ")
    for arr in fm.mergePick:
        print(arr.printStr())

    print("\nVariable Projection: ")
    for variable in fm.varProjFromMerge:
        print("variable "+ variable + ": ")
        arrList = fm.varProjFromMerge[variable]
        for arr in arrList:
            print(arr.printStr())

    print("\nVar Bank: ")
    for variable in fm.varMapBank:
        print("variable " + variable + ": ")
        arrList = fm.varMapBank[variable]
        for arr in arrList:
            print(arr.printStr())
            print(arr.checkUniqueness())
            # print(arr.checkNeighboring())
            # print(arr.checkConsistency())

    print("\nVar Map Pick: ")
    for variable in fm.varMapPick:
        print("variable " + variable + ": ")
        print(fm.varMapPick[variable].printStr())


    print("\nRewrite: ")
    for equation in fm.rwArrgmt:
        print("Left: " + equation[0].printStr())
        print("Right: " + equation[1].printStr())
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