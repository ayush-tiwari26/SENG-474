# classlist.py
# SENG 474
# Jeremy Ho & Helen Lin

import math, string

# Creates a decision tree using SLIQ
# Output:
# self.leafConnect
#	- an array of [ parent, child ] pairs
#	ie: [							Creates this tree structure
#				[ 1, 2 ]						1
#				[ 1, 3 ]					/   |   \
#				[ 2, 4 ]				   2    3    5
#				[ 1, 5 ]				  /
#		]								 4
#
# self.leaves
# 	- an array of leaves associated their attribute value and determines if it is the final class
# ie:
# [
# 	[ 2, "sunny", "" ],			<- tells us it's not the leaf node
# 	[ 3, "overcast", "yes" ]	<- tells us it is the leaf node and what class it is
# ]
class classlist:
	"Creates the decision tree."

	# d - The input data
	# The last column is the prediction category
	# Example: ( 2 records )
	# [
	# 	[ age, salary, marital, car ],
	# 	[ age, salary, marital, car ]
	# ]
	def __init__(self, d):
		self.data = d
		self.addID()
		self.classList = []
		self.attrList = []
		self.uniqueClassValues = []
		self.newLeaf = 1;
		self.tree = []
		self.leaves = []
		self.leafConnect = []
		
		self.init()
		self.totalRecords = len( self.classList )
		self.doSLIQ( self.attrList, 1, 1 )

		
	# Creates the classlist and attributeList
	# Example: ( 2 records )
	#
	# Attribute List:
	# [
	#	[ rid, age, salary, marital ],
	#	[ rid, age, salary, marital ]
	# ]
	#
	# Class List: 
	# [
	#	[ rid, car, leaf ],
	#	[ rid, car, leaf ]
	# ]
	#DONE
	def init( self ):
		classValues = []
		
		for row in self.data:
			#
			print(row)
			#
			self.attrList.append( row[0: len(row) - 1] )
			self.classList.append( [ row[0], row[len(row) - 1], self.newLeaf ] )
			classValues.append( row[len(row) - 1] )
				
		self.uniqueClassValues = list( set( classValues ) )
		self.newLeaf += 1
	
	
	# Adds rid to each record
	# Example: ( 2 records )
	# [
	# 	[ rid, age, salary, marital, car ],
	# 	[ rid, age, salary, marital, car ]
	# ]
	#DONE
	def addID( self ):
		for i in range( len(self.data) ):
			self.data[i].insert( 0, i )
	
	#DONE
	# Sorts the atrribute list base on the column number
	def sortList( self, attributeList, columnNumber ):
		attributeList.sort( key=lambda value: value[columnNumber] )
	
	
	#DONE
	# Returns an list of values of a single attribute
	def getSingleAttrList( self, leafList, colIndex ):
		aList = []
		for record in leafList:
			aList.append( record[colIndex] )
		return aList
	
	
	# Returns a record from a list with matching rid
	# The list is either attribute list or classlist
	#DONE
	def getRecordBaseOnRID( self, aList, rid ):
		for record in aList:
			if record[0] == rid:
				return record
				
	# DONE
	# Returns the class of a record
	def getClassByRID( self, rid ):
		
		for record in self.classList:
			if record[0] == rid:
				return record[1]
	
	#DONE
	# set leaf by rid
	def setLeafByRID( self, rid, leafNumber ):
		for record in self.classList:
			if record[0] == rid:
				record[2] = leafNumber
	
	#DONE
	# Returns attribute records with the same leaf number
	def getAttrListBaseOnLeaf( self, aList, leaf ):
		newAttrList = []
		for record in self.classList:
			if record[2] == leaf:
				newAttrList.append( self.getRecordBaseOnRID( aList, record[0] ) )
		return newAttrList
	
	#DONE
	def removeAttr( self, aList, colIndex ):
		newList = []
		for record in aList:
			newList.append( record[0:colIndex] + record[colIndex+1:] )
		return newList
	
	
	# Initialize an histogram structure
	# Eaxmple: n = 2, len( self.uniqueClassValues ) = 3
	# [
	#		[	0, 0, 0	]
	#		[	0, 0, 0	]
	# ]
	#DONE
	def createEmptyHistogram( self, n ):
		emptyHistogram = []
		
		for i in range( 0, n ):
			row = []
			for i in self.uniqueClassValues:
				row.append(0)
			emptyHistogram.append( row )
		return emptyHistogram
	
	# DONE
	def checkAllOneClass( self, newLeafAttrList ):
		currentClass = self.getClassByRID( newLeafAttrList[0][0] )
		for row in newLeafAttrList:
			if self.getClassByRID( row[0] ) != currentClass:
				return False, ""
		return True, currentClass
		
		
	# Returns the entropy calculated by the list of probabilities
	# make sure the list of probabilities sums up to total
	#DONE
	def calculateEntropy( self, probabilities, total ):
		entropy = float(0)
		if total != 0:
			for probability in probabilities:
				prob = float(probability) / float(total)
				if prob != 0:
					entropy += -1.0 *  prob  * math.log( prob, 2 )
		return entropy
		
		
	# Calculate the expected info of an attribute from a histogram
	# Example list
	# 			   		(	predictValue1, 	predictValue2, 	predictValue3  )
	#					[
	# (attrValue1)		[	1,				2,				3  				]
	# (attrValue2)		[	3,				4,				6  				]	
	#					]
	def calculateExpectedInfo( self, histogramList ):
		expectedInfo = 0
		for attrValueRow in histogramList:
			listSum = sum( attrValueRow )
			expectedInfo += ( float(listSum) / float(self.totalRecords) ) * self.calculateEntropy( attrValueRow, listSum )
		return expectedInfo
	
	
	# Perform SLIQ base on the provided attribute list of one type of leaf
	# Example of self.tree that will be poplated by this function
	# [
	#		[ level, leafNum, expectedInfo, attributeType, columnIndex, splitValue ]
	# [
	# level 				- which level of the tree this leaf is at
	# leafNum			- the leaf number
	# expectedInfo		- expectedInfo of this attribute
	# attributeType	- either numeric of category
	# columnIndex		- the index of the attribute in attrlist
	# splitAtValue		- the value(s) the attribute splite at 
	#						  if numeric, use <= as the comparing operater
	#						  if categorical, a list of values will be given
	def doSLIQ( self, attrLeafList, leafNum, level ):
		info = []					# holds all the expected info that have been calculated

		# starting with the first attribute at index 1
		for i in range( 1, len(attrLeafList[0]) ):			
			self.sortList( attrLeafList, i )
			if attrLeafList[0][i].isdigit():
				# do numerical calculation
				info.append( self.numericalCalculation( attrLeafList, i ) )
			else:	# do categorical calculation
				info.append( self.categoricalCalculation( attrLeafList, i ) )
				
		# sort the gathered info values
		self.sortList( info, 0 )
		bestInfo = info[0]
		bestInfo.insert( 0, leafNum )
		bestInfo.insert( 0, level )
		self.tree.append( bestInfo )
				
		# update leaf number
		newLeaves = self.updateLeaf( bestInfo, attrLeafList )
		
		# remove the used attribute and find the next level leaves
		if len( attrLeafList[0] ) > 2:
			newAttrList = self.removeAttr( attrLeafList, bestInfo[4] )
			for newLeaf in newLeaves:
				newLeafAttrList = self.getAttrListBaseOnLeaf( newAttrList, newLeaf[0] )
				self.leafConnect.append( [leafNum, newLeaf[0]] )
				if len(newLeafAttrList) != 0 and newLeaf[2] == "":
					self.doSLIQ( newLeafAttrList, newLeaf[0], level + 1 )
			
		self.leaves.extend( newLeaves )
		return
		
		
	# Updates the leaf number accoriding to the expected info given
	# Example of the input variable info
	# [ level, leafNum, expectedInfo, attributeType, columnIndex, splitValue ]
	#
	# Example of the output newLeaves:
	# [
	# 		[ newLeafNumber, splitCondition ]
	# ]
	def updateLeaf( self, info, attrLeafList ):
		newLeaves = []
		splitValue = info[5]
		
		# creating new leaf numbers
		if info[3] == "category":
			for value in splitValue:
				newLeaves.append( [self.newLeaf, value, ""] )
				self.newLeaf += 1
		else:
			newLeaves.append( [ self.newLeaf, "<= " + splitValue, "" ] )
			self.newLeaf += 1
			newLeaves.append( [ self.newLeaf, "> " + splitValue, "" ] )
			self.newLeaf += 1
		
		
		# updating leaf number
		for record in attrLeafList:
			if info[3] == "category":
				self.setLeafByRID( record[0], newLeaves[splitValue.index( record[info[4]] )][0] )				
			else:
				if record[info[4]] <= splitValue:
					self.setLeafByRID( record[0], newLeaves[0][0] )
				else:
					self.setLeafByRID( record[0], newLeaves[1][0] )
		
		# checking if the leaf numbers are final
		for newLeaf in newLeaves:
			newLeafAttrList = self.getAttrListBaseOnLeaf( attrLeafList, newLeaf[0] )
			result, leafClass = self.checkAllOneClass( newLeafAttrList )
			if result:
				newLeaf[2] = leafClass

		return newLeaves
	
	
	# Returns the expected info for this categorical attribute
	# Eaxample output:
	# [ expectedInfo, "category", columnIndex ] 
	def categoricalCalculation( self, leafList, colIndex ):
		attrUniqueValues = list( set(self.getSingleAttrList( leafList, colIndex )) )
		histogram = self.createEmptyHistogram( len(attrUniqueValues) )
		
		for row in leafList:
			attrValueIndex = attrUniqueValues.index( row[colIndex] )
			classValueIndex = self.uniqueClassValues.index( self.getClassByRID( row[0] ) )
			histogram[attrValueIndex][classValueIndex] += 1
		
		return [ self.calculateExpectedInfo( histogram ), "category", colIndex, attrUniqueValues ]
		
		
	# Returns the expected info for this numerical attribute
	# Eaxample output:
	# [ expectedInfo, "numeric", columnIndex, split at value ] 
	def numericalCalculation( self, leafList, colIndex ):
		infoList = []
		for splitRow in leafList:
			splitValue = splitRow[colIndex]
			histogram = self.createEmptyHistogram( 2 )
			
			for row in leafList:
				classValueIndex = self.uniqueClassValues.index( self.getClassByRID( row[0] ) )
				if row[colIndex] <= splitValue:
					histogram[0][classValueIndex] += 1
				else:
					histogram[1][classValueIndex] += 1
						
			infoList.append( self.calculateExpectedInfo( histogram ) )
				
		bestInfo = min( infoList )
		bestInfoIndex = infoList.index( bestInfo )
				
		return [ bestInfo, "numeric", colIndex, leafList[bestInfoIndex][colIndex] ]
	
	
	def displayTree( self ):
		print("Tree Structure:")
		self.sortList( self.leafConnect, 0 )
		currentNode = 0
		childNodes = ""
		for pair in self.leafConnect:
			if currentNode != pair[0]:
				if currentNode != 0:
					print("N{0} have the following children: {1}".format( currentNode, childNodes.lstrip(', ') ))
				currentNode = pair[0]
				childNodes = ""
			childNodes += ", N{0}".format( pair[1] )
		print("N{0} have the following children: {1}".format( currentNode, childNodes.lstrip(', ') ))
		
		print("\nNode Properties:")
		self.sortList( self.leaves, 0 )
		for node in self.leaves:
			if node[2] == "":
				print("N{0} is determined when attribute value is '{1}'".format( node[0], node[1]))
			else:
				print("N{0} is determined when attribute value is '{1}' and have class '{2}'".format( node[0], node[1], node[2]))
		return ""

"""
def main():
	data = [
		[ "Sunny", "17", "High", "False", "No" ],
		[ "Sunny", "20", "High", "True", "No" ],
		[ "Overcast", "23", "High", "False", "Yes" ],
		[ "Rainy", "32", "High", "False", "Yes" ],
		[ "Rainy", "43", "Normal", "False", "Yes" ],
		[ "Rainy", "68", "Normal", "True", "No" ],
		[ "Overcast", "17", "Normal", "True", "Yes" ],
		[ "Sunny", "20", "High", "False", "No" ],
		[ "Sunny", "23", "Normal", "False", "Yes" ],
		[ "Rainy", "32", "Normal", "False", "Yes" ],
		[ "Sunny", "43", "Normal", "True", "Yes" ],
		[ "Overcast", "68", "High", "True", "Yes" ],
		[ "Overcast", "17", "Normal", "False", "Yes" ],
		[ "Rainy", "20", "High", "True", "No" ]
	]
	data2 = [
		[ "23", "Family", "HIGH" ],
		[ "17", "Sports", "HIGH" ],
		[ "43", "Sports", "HIGH" ],
		[ "68", "Family", "LOW" ],
		[ "32", "Truck", "LOW" ],
		[ "20", "Family", "HIGH" ]
	]
	CL = classlist(data)
	print CL.leaves
	print CL.displayTree()
			
if __name__ == '__main__':
	main()
"""
