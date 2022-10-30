import math
import numpy as np
from utils import utils
class sliq:
    def __init__(self, dataset):
        self.utils = utils()
        self.classList = list()
        self.attributeList = list()
        self.uniqueClasses = list()
        self.leafCount = 1
        self.tree = list()
        self.leaves = list()
        self.leafConnect = list()

        i = 0
        while i<len(dataset):
            dataset[i].insert(0, i)
            i+=1

        classSet = set()
        for i in range(len(dataset)):
            item = dataset[i]
            self.attributeList.append(item[0: len(item) - 1])
            self.classList.append([item[0], item[len(item) - 1], self.leafCount])
            classSet.add(item[len(item) - 1])

        self.totalRecords = len(self.classList)
        self.uniqueClasses = list(classSet)
        self.leafCount += 1

        self.createSLIQ(self.attributeList, 1, 1)

    def checkAllOneClass(self, newLeafAttributeList):
        currentClass = self.utils.getClassByID(newLeafAttributeList[0][0], self.classList)
        for item in newLeafAttributeList:
            if self.utils.getClassByID(item[0], self.classList) != currentClass:
                return False, ""
        return True, currentClass

    # Returns the entropy calculated by the list of probabilities
    # make sure the list of probabilities sums up to total
    # DONE
    def calculateEntropy(self, probabilities, total):
        entropy = float(0)
        if total != 0:
            for probability in probabilities:
                prob = float(probability) / float(total)
                if prob != 0:
                    entropy += -1.0 * prob * math.log(prob, 2)
        return entropy

    # Calculate the expected metadata of an attribute from a histogram
    # Example list
    # 			   		(	predictValue1, 	predictValue2, 	predictValue3  )
    # [
    # (attrValue1)		[	1,				2,				3  				]
    # (attrValue2)		[	3,				4,				6  				]
    # ]
    def calculateExpectedInfo(self, histogramList):
        expectedInfo = 0
        for attrValueRow in histogramList:
            listSum = sum(attrValueRow)
            expectedInfo += (float(listSum) / float(self.totalRecords)) * self.calculateEntropy(attrValueRow, listSum)
        return expectedInfo


    def createSLIQ(self, attributeLeafList, leafNum, level):
        metadata = list()					
        # all the expected metadata that have been calculated
        # starting with the first attribute at index 1
        for i in range(1, len(attributeLeafList[0])):
            self.utils.sortListByColumn(attributeLeafList, i)
            if attributeLeafList[0][i].isdigit():
                # do numerical calculation
                metadata.append(self.numericalCalculation(attributeLeafList, i))
            else:  # do categorical calculation
                metadata.append(self.categoricalCalculation(attributeLeafList, i))
        # sort the gathered metadata values
        self.utils.sortListByColumn(metadata, 0)
        bestInfo = metadata[0]
        bestInfo.insert(0, leafNum)
        bestInfo.insert(0, level)
        self.tree.append(bestInfo)
        # update leaf number
        newLeaves = self.updateLeaf(bestInfo, attributeLeafList)
        # remove the used attribute and find the next level leaves
        if len(attributeLeafList[0]) > 2:
            newAttributes = self.utils.removeAttribute(attributeLeafList, bestInfo[4])
            for newLeaf in newLeaves:
                newLeafAttributeList = self.utils.getAttributeListBaseOnLeaf(
                    newAttributes, newLeaf[0], self.classList)
                self.leafConnect.append([leafNum, newLeaf[0]])
                if len(newLeafAttributeList) != 0 and newLeaf[2] == "":
                    self.createSLIQ(newLeafAttributeList, newLeaf[0], level + 1)

        self.leaves.extend(newLeaves)
        return

    def updateLeaf(self, metadata, attributeLeafList):
        newLeaves = list()
        splitValue = metadata[5]
        # creating new leaf numbers
        if metadata[3] == "catagorial":
            for value in splitValue:
                newLeaves.append([self.leafCount, value, ""])
                self.leafCount += 1
        else:
            newLeaves.append([self.leafCount, "<= " + splitValue, ""])
            self.leafCount += 1
            newLeaves.append([self.leafCount, "> " + splitValue, ""])
            self.leafCount += 1

        # updating leaf number
        for record in attributeLeafList:
            if metadata[3] == "catagorial":
                self.utils.setLeafByID(
                    record[0], newLeaves[splitValue.index(record[metadata[4]])][0], self.classList)
            else:
                if record[metadata[4]] <= splitValue:
                    self.utils.setLeafByID(record[0], newLeaves[0][0], self.classList)
                else:
                    self.utils.setLeafByID(record[0], newLeaves[1][0], self.classList)

        # checking if the leaf numbers are final
        for newLeaf in newLeaves:
            newLeafAttributeList = self.utils.getAttributeListBaseOnLeaf(attributeLeafList, newLeaf[0], self.classList)
            result, leafClass = self.checkAllOneClass(newLeafAttributeList)
            if result:
                newLeaf[2] = leafClass
        return newLeaves

    def categoricalCalculation(self, leafList, columnIndex):
        attributeUniqueValues = list(set(self.utils.getAttributeByColumn(leafList, columnIndex)))
        histogram = self.utils.createEmptyHistogram(len(attributeUniqueValues), self.uniqueClasses)
        for item in leafList:
            attrValueIndex = attributeUniqueValues.index(item[columnIndex])
            classValueIndex = self.uniqueClasses.index(
                self.utils.getClassByID(item[0], self.classList))
            histogram[attrValueIndex][classValueIndex] += 1

        return [self.calculateExpectedInfo(histogram), "catagorial", columnIndex, attributeUniqueValues]


    def numericalCalculation(self, leafList, columnIndex):
        infoList = list()
        for splitRow in leafList:
            splitValue = splitRow[columnIndex]
            histogram = self.utils.createEmptyHistogram(2, self.uniqueClasses)

            for item in leafList:
                classValueIndex = self.uniqueClasses.index(
                    self.utils.getClassByID(item[0], self.classList))
                if item[columnIndex] <= splitValue:
                    histogram[0][classValueIndex] += 1
                else:
                    histogram[1][classValueIndex] += 1

            infoList.append(self.calculateExpectedInfo(histogram))

        bestInfo = min(infoList)
        bestInfoIndex = infoList.index(bestInfo)

        return [bestInfo, "numeric", columnIndex, leafList[bestInfoIndex][columnIndex]]

    def display(self):
        print("Tree Structure:")
        self.utils.sortListByColumn(self.leafConnect, 0)
        currentNode = 0
        childNodes = ""
        for pair in self.leafConnect:
            if currentNode != pair[0]:
                if currentNode != 0:
                    print("Node {0} have the following children: {1}".format(
                        currentNode, childNodes.lstrip(', ')))
                currentNode = pair[0]
                childNodes = ""
            childNodes += ", Node {0}".format(pair[1])
        print("Node {0} have the following children: {1}".format(
            currentNode, childNodes.lstrip(', ')))

        print("\nNode Properties:")
        self.utils.sortListByColumn(self.leaves, 0)
        for node in self.leaves:
            if node[2] == "":
                print("Node{0} is triggered when attribute value is '{1}'".format(
                    node[0], node[1]))
            else:
                print("Node{0} is triggered when attribute value is '{1}' and have class {2}".format(
                    node[0], node[1], node[2]))
        return ""
