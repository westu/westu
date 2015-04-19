class record(object):
	def __init__(self, line):
		tmpData = line.strip().split(',')
		tmpType = int(tmpData[0])
		tmpAttributes = []
		for i in xrange(1, len(tmpData)):
			tmpAttributes.append(float(tmpData[i]))
		
		self.type = tmpType
		self.attributes = tmpAttributes

	def cal_distence(self, otherRecord):
		dis = 0
		for i in xrange(len(self.attributes)):
			dis += (self.attributes[i] - otherRecord.attributes[i]) ** 2
		dis = dis ** 0.5
		return dis

class kNN_Classifier(object):
	def __init__(self):
		self.data = []
		self.typeNumbers = 0

	def train(self, lines):
		for l in lines:
			self.data.append(record(l))
		
		for i in xrange(len(self.data)): #assumse we don't need to discretize the type data
			if self.data[i].type > self.typeNumbers:
				self.typeNumbers = self.data[i].type

	def find_k_nearest_neighbor(self, testLine, k):
		testData = record(testLine)
		tmpDisList = []
		for r in self.data:
			tmpDisList.append(r.cal_distence(testData))

		sortedList = sorted(tmpDisList) #will be optimized
		kNNList = []
		eps = 1e-6
		for i in xrange(len(tmpDisList)):
			if tmpDisList[i] <= sortedList[k - 1] or abs(tmpDisList[i] - sortedList[k - 1]) < eps:
			# the (k - 1)th means the kth number in sortedList
				kNNList.append(self.data[i].type)

		if len(kNNList) != k:
			print 'error of find_k_nearest_neighbor!', len(kNNList)
		return self.vote(kNNList)

	def vote(self, kNNList):
		voteBox = []
		for i in xrange(self.typeNumbers + 1): #python list numbers from 0, so we use [0..n]
			voteBox.append(0)

		#print self.typeNumbers
		for i in kNNList:
			#print i
			voteBox[i] = voteBox[i] + 1

		maxNum = 0
		for i in xrange(len(voteBox)):
			#print voteBox[i], maxNum
			if voteBox[i] > maxNum:
				maxNum = voteBox[i]
				voteResult = i
				#print voteResult

		return voteResult