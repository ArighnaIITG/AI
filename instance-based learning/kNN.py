"""
Simple example of kNN implemented from Scratch in Python
@author: Fernando Lovera
@date: Wed 25 Mar
@place: Caracas
""" 
import csv
import random
import math
import operator
"""
First open the file (filename) as csv. 
Then split the data in trainingSet(dataset) and test set.
We also need transform the string values into numbers 
that we can work with.
"""
def loadDataset(filename, split, trainingSet = [] , testSet = []):
	with open(filename, 'rb') as csvfile:
	    lines   = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y]  = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])
"""
To compare the similarities between two instances we use the euclidean
distance between bothe instances, which is defined as the square root of
the sum of square differences between the two arrays of numbers.
The 'length' parameter will tell you how many of the parameters you are 
considering.
"""
def euclideanDistance(instance1, instance2, length):
	distance      = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
"""
Process of calculating the distance for all instances 
and selecting a subset with the smallest distance values.
"""
def getNeighbors(trainingSet, testInstance, k):
	distances          = []
	length             = len(testInstance)-1
	neighbors          = []
	for x in range(len(trainingSet)):
		dist           = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key = operator.itemgetter(1)) #sorting the distances by the dist value
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
"""
We need to devise a predicted response based on the neighbors
We can do this by allowing each neighbor to vote for their class attribute,
and take the majority vote as the prediction.
"""
def getResponse(neighbors):
	classVotes   = {} # dictionary
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response]  = 1
	sortedVotes                   = sorted(classVotes.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sortedVotes[0][0]
def getAccuracy(testSet, predictions):
	correct               = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct      += 1
	return (correct/float(len(testSet))) * 100.0
	
def main():
	# prepare data
	trainingSet = []
	testSet     = []
	split       = 0.67 # convenient value to split the data
	loadDataset('iris.data', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions = []
	k           = 3 # get the 3 closest neighbourns
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result    = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
main()