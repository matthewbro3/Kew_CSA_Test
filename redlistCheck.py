#!/usr/bin/env python3
import sys, math
import matplotlib.pyplot as plt

check = sys.argv[1]
red = sys.argv[2]
growth = sys.argv[3]
"""
Define the first argument as the checklist file name ("check"), the second argument as the IUCN Red list filename ("red"), and the third argument as the growth forms list file name ("growth").
DO NOT put in the arguments in the wrong order.  The program will not function properly.
"""

def listRows(file):
	"""
	Counts the number of rows in a csv file.
	Subtracts 1 from the final count to account for the column header row.
	"""
	with open(file) as f:
		count = 0
		for line in f.readlines():
			count += 1
		return count -1

def compareRows(check, red):
	"""
	Indexes individual plant names from the checklist file and the IUCN redlist file into separate global lists.
	Checks the lists for each file against each other for matches.
	Returns final count of number of matches.
	Creates global lists of all plant names in the checklist and IUCN Red List for later use by other functions.
	DO NOT put the arguments in backwards.  The program will not function properly.
	NOTE: The program only logs exact matches. If a plant name is misspelled in one list, it will not be logged as appearing in both.  Ensure sanitized data inputs.
	NOTE: The program does not account for duplicate entries in the input files.  Duplicate entries may inflate the count of matches.  Run dupCheck function on input files to ensure there are no duplicates.
	NOTE: This function is designed to erase and rewrite the global lists it generates when run.
	If modifying this code, the developer advises against running this function more than once.
	"""
	global checkList
	global listRed
	checkList = []
	redList = []
	matches = 0
	with open(check) as c:
		for checkLine in c.readlines():
			checkName = checkLine.split(',')
			checkList.append(checkName[1])
	with open(red) as r:
		for redLine in r.readlines():
			redName = redLine.split(',')
			redList.append(redName[2])
	for name in checkList:
		if name in redList:
			matches += 1
	return matches
	
def dupCheck(doc, col):
	"""
	Debug function.
	Checks for duplicate names in designated column (col) of .csv file (doc).
	Functions by making sure the length of the whole list is the same as the length of the set of the list.
	Use to ensure input files do not contain duplicate entries, or two different entries for the same plant.
	"""
	docList = list()
	with open(doc) as f:
		for l in f.readlines():
			name = l.split(',')
			docList.append(name[col])
		if len(docList) != len(set(docList)):
			print("Duplicates Detected")

def compareRowsDEBUG(check, red):
	"""
	Indexes every name in the second column of the checklist file.
	Checks to see if that name appears in the redlist file.
	NOTE: The program only logs exact matches. If a plant name is misspelled in one list, it will not be logged as appearing in both.  Ensure sanitized data inputs.
	FOR DEBUG PURPOSES ONLY
	This function is meant to check the veracity of the primary compareRows function.
	If it returns a different number than the primary compareRows function, one or both functions are making a mistake in their count.
	"""
	with open(check) as c:
		count = 0
		for checkLine in c.readlines():
			checkName = checkLine.split(',')
			with open(red) as r:
				redRead = r.readlines()
				for redLine in redRead:
					redName = redLine.split(',')
					if checkName[1] == redName[2]:
						count += 1
	return count

def threatCheck(file):
	"""
	Finds all plants in the IUCN Red List file that are in a threatened category (vulnerable, endangered, or critically endangered), appends them to a global list for use by other functions.
	Returns the number of threatened species.
	NOTE: This function is designed to erase and rewrite the global list of threatened plants when run.
	If modifying this code, the developer advises against running this function more than once.
	"""
	global threatList
	threatList = []
	with open(file) as f:
		for line in f.readlines():
			entry = line.split(',')
			if entry[3] == 'Vulnerable' or entry[3] == 'Endangered' or entry[3] == 'Critically Endangered':
				threatList.append(entry[2])
	return len(threatList)

def treeCheck(file):
	"""
	Creates a global list of the scientific names of all trees in the growth forms file.
	Returns the number of trees.
	NOTE: This function is designed to erase and rewrite the global list of trees when run.
	If modifying this code, the developer advises against running this function more than once.
	"""
	global treeList
	treeList = []
	with open(file) as f:
		for line in f.readlines():
			entry =  line.split(',')
			if "Tree" in entry[4]:
				treeList.append(entry[2])
	return len(treeList)
	
def treeThreat():
	"""
	Compares the list of threatened plants to the list of trees and returns the number of threatened trees.
	Writes the names of all threatened trees to a global list
	NOTE: This function requires the global list of trees and the global list of threatened plants to both have been defined.
	If modifying this code, only run this after having run the treeCheck and threatCheck functions first.
	"""
	global treeThreatList
	treeThreatList = []
	count = 0
	for name in threatList:
		if name in treeList:
			count += 1
			treeThreatList.append(name)
	return count
		

"""
print("Checking List 1")
dupCheck(check, 1)
print("Checking list 2")
dupCheck(red, 2)
threatCheck(redList)
Debug code, running debug function of dupCheck to check for duplicates.
"""

total = listRows(check)
assessed = compareRows(check, red)
threatened = threatCheck(red)
trees = treeCheck(growth)
threatenedTrees = treeThreat()
#runs all necessary functions; stores returned values as variables

pAssessed = assessed/total
pThreatened = threatened/assessed
pTrees = trees/assessed
pThreatenedTrees = threatenedTrees/assessed
pExpectedTrees = pTrees*pThreatened
#pTreesThreatened = threatenedTrees/threatened
#calculates decimal ratio values based on above variables; for variable ID, see below

print("Proportion of Assessed in Listed:", pAssessed)
print("Proportion of Threatened in Assessed:", pThreatened)
print("Proportion of Trees in Assessed:", pTrees)
print("Proportion of Threatened Trees in Assessed", pThreatenedTrees)
print("Expected Proportion of Threatened Trees in Assessed", pExpectedTrees)
#print("Proportion of Trees in Threatened", pTreesThreatened)
#prints above ratio values with appropriate labels

labels = ["Threatened", "Trees", "Threatened Trees,\nExpected", "Threatened Trees,\nActual"]
percentages = [pThreatened, pTrees, pExpectedTrees, pThreatenedTrees]
plt.bar(labels, percentages, width=0.8, bottom=None)
for x, y in enumerate(percentages):
	plt.text(x-0.2, y+0.01, str(round(y,4)))
plt.xticks(rotation=45, ha="right")
plt.ylabel("Ratio of Assessed Plants")
plt.ylim([0,1])
plt.tight_layout()
plt.show()
#plots the ratio values on a bar chart
