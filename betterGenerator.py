import constants
import random
import numpy as np
import csv

inputList = list()
outputList = list()

test_inputList = list()
test_outputList = list()

def generate_all(degree):
    # DATASET
    for index in range(0, constants.DATASET_SIZE):
        generate(degree)
    writeToFile(inputList, outputList)
    for index in range(0, constants.DATASET_SIZE // 5):
        generate(degree, test=True)
    writeToFile(test_inputList, test_outputList, test=True)


def generate(degree, test=False):
    # There must be at least 1 roots for a odd degree polynomial
    isOdd=degree % 2 == 1
    rootCounter = 0
    if isOdd:
        rootCounter = 1
    # Than I need an array that shows possible number of roots
    possibleNumberOfRoots = possibleRoots(degree=degree, isOdd=isOdd)
    complexPart = 0
    realPart = 0
    cof = list()
    for numberOfRealRoots in possibleNumberOfRoots:
        numberOfComplexRoots = (degree - numberOfRealRoots) // 2
        realPart = getRealMultiplication(numberOfRealRoots)
        rootClass = prepareForClassification(degree, int(numberOfRealRoots))
        if numberOfComplexRoots > 0:
            complexPart = getComplexMultiplication(numberOfPairs=numberOfComplexRoots, numberInterval=constants.MAX_INTEGER_VALUE)
            realPart = getRealMultiplication(numberOfRealRoots, numberInterval=constants.MAX_INTEGER_VALUE)
            cof = np.polymul(complexPart, realPart).coefficients
            if test:
                test_inputList.append(cof)
                test_outputList.append(rootClass)
            else:
                inputList.append(cof)
                outputList.append(rootClass)
        else:
            cof = np.polymul(np.poly1d(1), realPart).coefficients
            if test:
                test_inputList.append(cof)
                test_outputList.append(rootClass)
            else:
                inputList.append(cof)
                outputList.append(rootClass)


def prepareForClassification(degree, numberOfRoots):
    initial = 1 if degree % 2 == 1 else 0
    classNum = 0
    for i in range(initial, degree + 1, 2):
        if i == numberOfRoots:
            return classNum
        else:
            classNum += 1


def possibleRoots(degree, isOdd):
    # Odd degrees can have only odd number of roots
    incrementForMakingItOdd = 1 if isOdd else 0
    result = list()
    if isOdd:
        result.append(1)
    else:
        result.append(0)
    for i in range(2, degree+1, 2):
        result.append(i + incrementForMakingItOdd)
    return result


def getComplexMultiplication(numberOfPairs, numberInterval=100):
    complexPairs = list()
    for i in range(0, numberOfPairs):
        # In each pair I need two numbers
        first = random.randrange(-numberInterval, numberInterval)
        second = random.randrange(-numberInterval, numberInterval)
        while first == 0 or second == 0:
            first = random.randrange(-numberInterval, numberInterval)
            second = random.randrange(-numberInterval, numberInterval)
        firstPoly = np.poly1d([1, first**2])
        secondPoly = np.poly1d([1, second**2])
        complexPairs.append(np.polymul(firstPoly, secondPoly))
        result = np.poly1d(1)
    if numberOfPairs == 1:
        result = complexPairs[0]
    else:
        for i in range(0, len(complexPairs) // 2 + 1, 2):
            tmp = np.polymul(complexPairs[i], complexPairs[i+1])
            result = np.polymul(result, tmp)
        if  len(complexPairs) % 2 == 1:
            result = np.polymul(result, complexPairs[len(complexPairs) - 1])
    
    return result


def getRealMultiplication(numberOfRoots, numberInterval=100):
    arr = random.sample(range(-numberInterval, numberInterval), numberOfRoots)
    for i in range(numberOfRoots - len(arr)):
        arr.append(arr[0])
    arr = random.sample(arr, len(arr))
    return np.poly1d(arr, True)  


def writeToFile(input, output, test=False):
    if test:
        inputName = "_coefficients.csv"
        outputName = "_numberOfRoots.csv"
    else:
        inputName = "coefficients.csv"
        outputName = "numberOfRoots.csv"
    with open(inputName, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(input)
    with open(outputName, "w") as o:
        np.savetxt(o, output, delimiter=',', fmt="%2d")


def main():
    generate_all(degree=10)


if __name__ == '__main__':
    main()
