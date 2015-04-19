def read_data():
	f = open('data.txt')
	lines = f.readlines()
	f.close()
	item_set = []
	record_set = []
	for l in lines:
		tmp_record_set = []
		tmp = l.strip().split(' ')
		for i in xrange(len(tmp)):
			item = int(tmp[i]) + 10 ** i
			tmp_record_set.append(item)
			if item not in item_set:
				item_set.append(item)
		record_set.append(tmp_record_set)
	return record_set, item_set

def frequence_check(item, record_set):
	frequence = 0
	for record in record_set:
		exist = True
		for i in item:
			# print i
			if i not in record:
				exist = False
				break
		if exist == True:
			frequence += 1
	# print float(frequence)
	return float(frequence) / len(record_set)

def main():
	record_set, item_set = read_data()
	for i in record_set:  # just for testing
		for j in i:
			print j,
		print

	min_sup = 0.28
	frequence_item_set = []
	for i in item_set:
		if frequence_check([i], record_set) >= min_sup:
			frequence_item_set.append([i])

	item_num = 0
	while True:
		item_num += 1
		tmp_item_set = []
		for i in frequence_item_set:
			if len(i) == item_num:
				tmp_item_set.append(i)
		if len(tmp_item_set) == 0:
			break

		for i in xrange(len(tmp_item_set) - 1):
			for j in xrange(i+1, len(tmp_item_set)):
				if common_expect_one(tmp_item_set[i], tmp_item_set[j]):
					tmp_new_item = set(tmp_item_set[i]) | set(tmp_item_set[j])
					# print tmp_new_item
					if (frequence_check(tmp_new_item, record_set) >= min_sup) \
					   and (tmp_new_item not in frequence_item_set):
						frequence_item_set.append(tmp_new_item)

	for i in frequence_item_set:
		if ((10000 in i) or (10001 in i)) and (len(i) >= 2):
			print i

def common_expect_one(set1, set2):
	differen1 = 0
	differen2 = 0
	for i in set1:
		if i not in set2:
			differen1 += 1
	for i in set2:
		if i not in set1:
			differen2 += 1
	# print set1, set2
	# print differen1, differen2
	return (differen1 == 1) and (differen2 == 1)

if __name__ == "__main__":
	main()