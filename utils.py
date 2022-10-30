class utils:
    # Sorts the atrribute list base on the column number
    def sortListByColumn(self, attributeList, columnNumber):
        attributeList.sort(key=lambda value: value[columnNumber])

    def removeAttribute(self, lst, columnIndex):
        newList = []
        for record in lst:
            newList.append(record[0:columnIndex] + record[columnIndex+1:])
        return newList
        
    # Returns an list of values of a single attribute
    def getAttributeByColumn(self, leafList, columnIndex):
        lst = []
        for record in leafList:
            lst.append(record[columnIndex])
        return lst

    def getRecordByID(self, lst, id):
        for record in lst:
            if record[0] == id:
                return record
    
    def getClassByID(self, id, classList):
        for record in classList:
            if record[0] == id:
                return record[1]
    
    def setLeafByID(self, id, leafNumber, classList):
        for record in classList:
            if record[0] == id:
                record[2] = leafNumber

    def getAttributeListBaseOnLeaf(self, lst, leaf, classList):
        newAttributes = []
        for record in classList:
            if record[2] == leaf:
                newAttributes.append(self.getRecordByID(lst, record[0]))
        return newAttributes

    def createEmptyHistogram(self, n, uniqueClasses):
        emptyHistogram = []
        for j in range(0, n):
            item = []
            for i in uniqueClasses:
                item.append(0)
            emptyHistogram.append(item)
        return emptyHistogram