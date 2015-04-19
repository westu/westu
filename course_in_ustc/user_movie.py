import numpy as np
import time
from sys import argv

class movie(object):
	def __init__(self, movieId, movieTitle, movieGenres):
		self.id = movieId
		self.title = movieTitle
		self.genres = []
		for i in movieGenres:
			self.genres.append(i)

def get_movies(fileName):	
	readFile = open(fileName)
	lines = readFile.readlines()
	readFile.close()

	movies = []
	moviesIndex = {}
	index = -1
	for l in lines:
		parts = l.strip().split('::')
		tmpMovie = movie(int(parts[0]), parts[1], parts[2].split('|'))
		movies.append(tmpMovie)
		index = index + 1
		moviesIndex[tmpMovie.id] = index

	return movies, moviesIndex

class class_user(object):
	def __init__(self, userId, gender, age):
		self.id = userId
		self.gender = gender
		self.ageRanges = {}
		self.age = age
		self.movieRating = {}
		self.genersRating = {}

	def get_movie_rating(self, movieId, movieRating):
		if movieId not in self.movieRating:
			self.movieRating[movieId] = []
		self.movieRating[movieId].append(movieRating)

	def cal_movie_rating(self):
		for i in self.movieRating:
			self.movieRating[i] = np.mean(self.movieRating[i])

	def get_genres_rating(self, movieId, movieRating, movies, moviesIndex):
		for gener in movies[moviesIndex[movieId]].genres:
			if gener not in self.genersRating:
				self.genersRating[gener] = []
			self.genersRating[gener].append(movieRating)

	def cal_genres_rating(self):
		for i in self.genersRating:
			self.genersRating[i] = np.mean(self.genersRating[i])

	def get_features(self, ratingLines, ratingLinesDict, movies, moviesIndex):
		i = ratingLinesDict[self.id]
		while True: # get the user's feature
			l = ratingLines[i]
			if not l.startswith(str(self.id)):
				break
			parts = l.strip().split('::')
			self.get_movie_rating(int(parts[1]), int(parts[2]))
			self.get_genres_rating(int(parts[1]), int(parts[2]), movies, moviesIndex)
			
			i = i + 1
			if i == len(ratingLines):
				break

		self.cal_movie_rating() 
		#get the average rating if somebody rates several times

		#self.cal_genres_rating()

def get_users(fileName, ratingLines, ratingLinesDict, movies, moviesIndex):
	readFile = open(fileName)
	lines = readFile.readlines()
	readFile.close()

	usersIndex = {}
	users = []
	index = 0
	for l in lines:
		parts = l.strip().split('::')
		tmpUser = class_user(int(parts[0]), parts[1], int(parts[2]))
		users.append(tmpUser)
		users[-1].get_features(ratingLines, ratingLinesDict, movies, moviesIndex)
		index = index + 1
		usersIndex[tmpUser.id] = index
		
	return users, usersIndex

class error(object):
	def __init__(self):
		self.errorInGender = 0
		self.errorInAge = 0
		self.testNum = 0

		self.ageRanges = {}
		tmp = [1, 18, 25, 35, 45, 50, 56]
		for i in xrange(len(tmp)):
			self.ageRanges[tmp[i]] = i

	def cal_error(self, testUser, predicGender, predicAge):
		self.testNum = self.testNum + 1
		if predicGender != testUser.gender:
			self.errorInGender = self.errorInGender + 1
		if predicAge < 18:
			pA = 0
		elif predicAge < 25:
			pA = 1
		elif predicAge < 35:
			pA = 2
		elif predicAge < 45:
			pA = 3
		elif predicAge < 50:
			pA = 4
		elif predicAge < 56:
			pA = 5
		else:
			pA = 6
		self.errorInAge = self.errorInAge + abs(pA - self.ageRanges[testUser.age])

def main():
	t1 = time.clock()
	movies, moviesIndex = get_movies('movies.dat')
	#moviesIndex is used to get the subscript of list movies when we have id

	readFile = open('ratings.dat')
	ratingLines = readFile.readlines()
	readFile.close()
	ratingLinesDict = {}
	for i in xrange(len(ratingLines)):
		tmp = int(ratingLines[i].strip().split('::')[0])
		if tmp not in ratingLinesDict: # the information of tmp starts at line i
			ratingLinesDict[tmp] = i
	t2 = time.clock()
	print 'pre-train time:', str(t2 - t1) + 's'
	print

	evaluationAll = error()
	for i in xrange(10): #10-fold cross validation
		t3 = time.clock()
		for j in xrange(10):
			if j != i:
				fileName = 'users.dat' + str(j)
				users, usersIndex = get_users(fileName, ratingLines, ratingLinesDict, movies, moviesIndex)
		t4 = time.clock()

		#test
		fileName = 'users.dat' + str(i)
		readFile = open(fileName)
		lines = readFile.readlines()
		readFile.close()

		evaluationThisFold = error()
		for l in lines:
			parts = l.strip().split('::')
			testUser = class_user(int(parts[0]), parts[1], int(parts[2]))
			testUser.get_features(ratingLines, ratingLinesDict, movies, moviesIndex)

			predicGender = 0
			predicAge = 0
			allWeightsInAge = 0
			for user in users:
				predicGender, predicAge, allWeightsInAge = get_similar_users(testUser, user, predicGender, predicAge, allWeightsInAge)

			if predicGender > 0:
				predicGender = 'M'
			else:
				predicGender = 'F'

			evaluationAll.cal_error(testUser, predicGender, predicAge)
			evaluationThisFold.cal_error(testUser, predicGender, predicAge)

		t5 = time.clock()

		print i, 'gender error:', str(float(evaluationThisFold.errorInGender) / evaluationThisFold.testNum) + '%', \
		      '\t age error:', float(evaluationThisFold.errorInAge) / evaluationThisFold.testNum
		print 'train time:', str(t4 - t3) + 's', '\t test time:', str(t5 - t4) + 's'
		print

	#the result
	print 'the whole gender error:', str(float(evaluationAll.errorInGender) / evaluationAll.testNum) + '%', \
		  '\t the whole age error:', float(evaluationAll.errorInAge) / evaluationAll.testNum
			
def get_similar_users(testUser, user, predicGender, predicAge, allWeightsInAge):

	commonGenerNum = 0
	for i in testUser.genersRating:
		if i in user.genersRating: #\
		#and abs(testUser.genersRating[i] - user.genersRating[i]) <= 1:
			commonGenerNum = commonGenerNum + 1
	if commonGenerNum < 8: # they arn't similar
		return predicGender, predicAge, allWeightsInAge

	differValue = 0 #the bigger, the more different
	for i in testUser.genersRating:
		if i in user.genersRating:
			differValue = differValue + min(10, abs(len(testUser.genersRating[i]) - len(user.genersRating[i])))

	if user.gender == 'M':
		tmp = 1.0
	else:
		tmp = -1.0
	predicGender = predicGender + tmp * 5.0 / differValue

	predicAge = predicAge * allWeightsInAge + user.age * 5.0 / differValue
	allWeightsInAge = allWeightsInAge + 5.0 / differValue
	predicAge = float(predicAge) / allWeightsInAge

	return predicGender, predicAge, allWeightsInAge

if __name__ == "__main__":
	#tmp, i = argv
	main()