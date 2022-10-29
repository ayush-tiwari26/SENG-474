import math
class sliq:
    def __init__(self, dataset):
        self.dataset = dataset
        self.setID()
        self.classList = []
        self.attributeList = []
        self.uniqueClasses = []
        self.newLeaf = 1
        self.tree = []
        self.leaves = []
        self.leafConnect = []

        self.initialize_options()
        self.totalRecords = len(self.classList)
        self.doSLIQ(self.attributeList, 1, 1)

    def initialize_options(self):
        classSet = set()
        for item in self.dataset:
            self.attributeList.append(item[0: len(item) - 1])
            self.classList.append([item[0], item[len(item) - 1], self.newLeaf])
            classSet.add(item[len(item) - 1])

        self.uniqueClasses = list(classSet)
        self.newLeaf += 1

    def setID(self):
        for i in range(len(self.dataset)):
            self.dataset[i].insert(0, i)

    # Sorts the atrribute list base on the column number
    def sortListByColumn(self, attributeList, columnNumber):
        attributeList.sort(key=lambda value: value[columnNumber])

    # Returns an list of values of a single attribute
    def getAttributeByColumn(self, leafList, columnIndex):
        lst = []
        for record in leafList:
            lst.append(record[columnIndex])
        return lst

    def getRecordByID(self, lst, rid):
        for record in lst:
            if record[0] == rid:
                return record

    # DONE
    # Returns the class of a record
    def getClassByID(self, rid):

        for record in self.classList:
            if record[0] == rid:
                return record[1]

    # DONE
    # set leaf by rid
    def setLeafByID(self, rid, leafNumber):
        for record in self.classList:
            if record[0] == rid:
                record[2] = leafNumber

    # DONE
    # Returns attribute records with the same leaf number
    def getAttrListBaseOnLeaf(self, lst, leaf):
        newAttributes = []
        for record in self.classList:
            if record[2] == leaf:
                newAttributes.append(self.getRecordByID(lst, record[0]))
        return newAttributes

    # DONE
    def removeAttr(self, lst, columnIndex):
        newList = []
        for record in lst:
            newList.append(record[0:columnIndex] + record[columnIndex+1:])
        return newList

    # Initialize an histogram structure
    # Eaxmple: n = 2, len( self.uniqueClasses ) = 3
    # [
    #		[	0, 0, 0	]
    #		[	0, 0, 0	]
    # ]
    # DONE
    def createEmptyHistogram(self, n):
        emptyHistogram = []

        for i in range(0, n):
            item = []
            for i in self.uniqueClasses:
                item.append(0)
            emptyHistogram.append(item)
        return emptyHistogram

    # DONE
    def checkAllOneClass(self, newLeafAttrList):
        currentClass = self.getClassByID(newLeafAttrList[0][0])
        for item in newLeafAttrList:
            if self.getClassByID(item[0]) != currentClass:
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

    # Calculate the expected info of an attribute from a histogram
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
            expectedInfo += (float(listSum) / float(self.totalRecords)) * \
                self.calculateEntropy(attrValueRow, listSum)
        return expectedInfo


    def doSLIQ(self, attrLeafList, leafNum, level):
        info = []					# holds all the expected info that have been calculated

        # starting with the first attribute at index 1
        for i in range(1, len(attrLeafList[0])):
            self.sortListByColumn(attrLeafList, i)
            if attrLeafList[0][i].isdigit():
                # do numerical calculation
                info.append(self.numericalCalculation(attrLeafList, i))
            else:  # do categorical calculation
                info.append(self.categoricalCalculation(attrLeafList, i))

        # sort the gathered info values
        self.sortListByColumn(info, 0)
        bestInfo = info[0]
        bestInfo.insert(0, leafNum)
        bestInfo.insert(0, level)
        self.tree.append(bestInfo)

        # update leaf number
        newLeaves = self.updateLeaf(bestInfo, attrLeafList)

        # remove the used attribute and find the next level leaves
        if len(attrLeafList[0]) > 2:
            newAttributes = self.removeAttr(attrLeafList, bestInfo[4])
            for newLeaf in newLeaves:
                newLeafAttrList = self.getAttrListBaseOnLeaf(
                    newAttributes, newLeaf[0])
                self.leafConnect.append([leafNum, newLeaf[0]])
                if len(newLeafAttrList) != 0 and newLeaf[2] == "":
                    self.doSLIQ(newLeafAttrList, newLeaf[0], level + 1)

        self.leaves.extend(newLeaves)
        return


    def updateLeaf(self, info, attrLeafList):
        newLeaves = []
        splitValue = info[5]

        # creating new leaf numbers
        if info[3] == "category":
            for value in splitValue:
                newLeaves.append([self.newLeaf, value, ""])
                self.newLeaf += 1
        else:
            newLeaves.append([self.newLeaf, "<= " + splitValue, ""])
            self.newLeaf += 1
            newLeaves.append([self.newLeaf, "> " + splitValue, ""])
            self.newLeaf += 1

        # updating leaf number
        for record in attrLeafList:
            if info[3] == "category":
                self.setLeafByID(
                    record[0], newLeaves[splitValue.index(record[info[4]])][0])
            else:
                if record[info[4]] <= splitValue:
                    self.setLeafByID(record[0], newLeaves[0][0])
                else:
                    self.setLeafByID(record[0], newLeaves[1][0])

        # checking if the leaf numbers are final
        for newLeaf in newLeaves:
            newLeafAttrList = self.getAttrListBaseOnLeaf(
                attrLeafList, newLeaf[0])
            result, leafClass = self.checkAllOneClass(newLeafAttrList)
            if result:
                newLeaf[2] = leafClass

        return newLeaves


    def categoricalCalculation(self, leafList, columnIndex):
        attrUniqueValues = list(
            set(self.getAttributeByColumn(leafList, columnIndex)))
        histogram = self.createEmptyHistogram(len(attrUniqueValues))

        for item in leafList:
            attrValueIndex = attrUniqueValues.index(item[columnIndex])
            classValueIndex = self.uniqueClasses.index(
                self.getClassByID(item[0]))
            histogram[attrValueIndex][classValueIndex] += 1

        return [self.calculateExpectedInfo(histogram), "category", columnIndex, attrUniqueValues]


    def numericalCalculation(self, leafList, columnIndex):
        infoList = []
        for splitRow in leafList:
            splitValue = splitRow[columnIndex]
            histogram = self.createEmptyHistogram(2)

            for item in leafList:
                classValueIndex = self.uniqueClasses.index(
                    self.getClassByID(item[0]))
                if item[columnIndex] <= splitValue:
                    histogram[0][classValueIndex] += 1
                else:
                    histogram[1][classValueIndex] += 1

            infoList.append(self.calculateExpectedInfo(histogram))

        bestInfo = min(infoList)
        bestInfoIndex = infoList.index(bestInfo)

        return [bestInfo, "numeric", columnIndex, leafList[bestInfoIndex][columnIndex]]

    def displayTree(self):
        print("Tree Structure:")
        self.sortListByColumn(self.leafConnect, 0)
        currentNode = 0
        childNodes = ""
        for pair in self.leafConnect:
            if currentNode != pair[0]:
                if currentNode != 0:
                    print("N{0} have the following children: {1}".format(
                        currentNode, childNodes.lstrip(', ')))
                currentNode = pair[0]
                childNodes = ""
            childNodes += ", N{0}".format(pair[1])
        print("N{0} have the following children: {1}".format(
            currentNode, childNodes.lstrip(', ')))

        print("\nNode Properties:")
        self.sortListByColumn(self.leaves, 0)
        for node in self.leaves:
            if node[2] == "":
                print("N{0} is determined when attribute value is '{1}'".format(
                    node[0], node[1]))
            else:
                print("N{0} is determined when attribute value is '{1}' and have class {2}".format(
                    node[0], node[1], node[2]))
        return ""
