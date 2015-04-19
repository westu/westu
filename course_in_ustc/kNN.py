import kNN_Classifier
import random

def test(lines):
	kNNClassifier = kNN_Classifier.kNN_Classifier()
	kNNClassifier.train(lines)

	for i in xrange(len(kNNClassifier.data)):
		t = kNNClassifier.find_k_nearest_neighbor(kNNClassifier.data[i], 1)
		if t != kNNClassifier.data[i].type:
			print i

def cross_check_data(lines):
	random.shuffle(lines)
	checkData = []
	tmp = int(len(lines) / 5)
	for i in xrange(5):
		checkData.append([])
		for j in xrange(tmp * i, tmp * (i + 1)): # [tmp * i .. tmp * (i + 1) - 1]
			checkData[i].append(lines[j])

	for j in xrange(tmp * 5, len(lines)): # the rest of lines, the part of (tmp % 5) 
		checkData[4].append(lines[j])

	return checkData

if __name__ == "__main__":
	readFileName = raw_input('Please input the file name:')
	file = open(readFileName)
	lines = file.readlines()
	file.close()
	#test(lines) # when k = 1, the answer must be itself

	checkData = cross_check_data(lines)

	minError = -1
	for k in xrange(1, int(len(lines) / 5 * 4)):
		errorNum = 0
		for i in xrange(5):
			testData = checkData[i]
			trainData = []
			for j in xrange(5):
				if j != i:
					trainData = trainData + checkData[j]

			kNNClassifier = kNN_Classifier.kNN_Classifier()
			kNNClassifier.train(trainData) # get a kNN classifier

			for j in testData:
				tmpOut = kNNClassifier.find_k_nearest_neighbor(j, k)
				if tmpOut != kNN_Classifier.record(j).type:
					errorNum = errorNum + 1
		# errorNum = float(errorNum) / 5

		print k, 'error rate:', errorNum * 1.0 / len(lines) # print the error ratio
		if (minError == -1) or (errorNum < minError):
			minError = errorNum
			minK = k

	print 'minErrorNum & minK:', minError, minK
	