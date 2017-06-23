from scipy import spatial
class variante:		

	def __init__(self, variant, prob, cases):
		self.variant = variant
		self.data = []
		self.contador = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.constant = 	['A_Create Application',
						 	'A_Submitted',
						 	'A_Concept',
						 	'W_Complete application',
						 	'A_Accepted',
						 	'O_Create Offer',
						 	'O_Created',
						 	'O_Sent (mail and online)',
						 	'W_Call after offers',
						 	'A_Complete',
						 	'W_Validate application',
						 	'A_Validating',
						 	'O_Returned',
						 	'W_Call incomplete files',
						 	'A_Incomplete',
						 	'O_Accepted',
						 	'A_Pending',
						 	'A_Denied',
						 	'O_Refused',
							'O_Cancelled',
						 	'W_Handle leads',
						 	'A_Cancelled',
							'O_Sent (online only)',
							'W_Assess potential fraud',
						 	'W_Personal Loan collection',
							'W_Shortened completion']
		self.prob = prob
		self.cases = cases
		self.prediction = 0
	def add_data(self, data):
		self.data.append(data)
		for i in range(26):
			if data == self.constant[i]:
				self.contador[i] = self.contador[i] +1
	def get_data(self):
		return self.data
	def get_contador(self):
		return self.contador
	def get_similarity(self, other):
		result = 1 - spatial.distance.cosine(self.contador, other.get_contador())
		result = result + self.check_conformance(other)
		return result / 2
	def check_conformance(self, other):
		min_len = len(self.data)
		max_len = len(self.data)
		other_data = other.get_data()
		if len(other_data)<min_len:
			min_len = len(other_data)
		else: 
			max_len = len(other_data)
		match = 0
		for i in range(min_len):
			if self.data[i] == other_data[i]:
				match = match +1
		return match / max_len

	def get_similarity_trunc(self, other, trunc):
		my_data = self.data[:]
		other_data = other.get_data()[:]

		if trunc < len(my_data):
			for i in range(len(my_data)-trunc):
				my_data.pop()

		if trunc < len(other_data):
			for i in range(len(other_data)-trunc):
				other_data.pop()

		my_contador = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		other_contador = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

		for i in my_data:
			for j in range(26):
				if i == self.constant[j]:
					my_contador[j] = my_contador[j] +1

		for i in other_data:
			for j in range(26):
				if i == self.constant[j]:
					other_contador[j] = other_contador[j] +1

		result = 1 - spatial.distance.cosine(my_contador, other_contador)
		result = result + self.check_conformance_trunc(my_data, other_data)
		return result / 2

	def check_conformance_trunc(self, my_data, other_data):
		min_len = len(my_data)
		max_len = len(my_data)
		other_data = other_data
		if len(other_data)<min_len:
			min_len = len(other_data)
		else: 
			max_len = len(other_data)
		match = 0
		for i in range(min_len):
			if my_data[i] == other_data[i]:
				match = match +1
		return match / max_len


def obtener_pred(recommender, number):
	for i in range(0,1000):
		maxi = 0
		sim = [0]*4047
		actual = 0
		five = [0]*5
		for j in range(1000,4047):
			sim[j] = recommender[number[i]].get_similarity(recommender[number[j]])
		for k in range(5):
			maxi = 0
			actual = 0
			for j in range(1000,4047):
				if j==five[0] or j==five[1] or j==five[2] or j==five[3] or j==five[4]:
					continue
				if maxi < sim[j]:
					maxi = sim[j]
					actual = number[j]
			if five[0] == 0:
				five[0]=actual
			elif five[1] == 0:
				five[1] = actual
			elif five[2] == 0:
				five[2] = actual
			elif five[3] == 0:
				five[3] = actual
			elif five[4] == 0:
				five[4] = actual
		total_cases = recommender[five[0]].cases + recommender[five[1]].cases + recommender[five[2]].cases + recommender[five[3]].cases + recommender[five[4]].cases
		recommender[number[i]].prediction = (recommender[five[0]].prob * recommender[five[0]].cases+ 
										recommender[five[1]].prob * recommender[five[1]].cases+
										recommender[five[2]].prob * recommender[five[2]].cases+
										recommender[five[3]].prob * recommender[five[3]].cases+
										recommender[five[4]].prob * recommender[five[4]].cases)/total_cases
def obtener_pred_trunc(recommender, number, trunc):
	for i in range(0,1000):
		maxi = 0
		sim = [0]*4047
		actual = 0
		five = [0]*5
		for j in range(1000,4047):
			sim[j] = recommender[number[i]].get_similarity_trunc(recommender[number[j]], trunc)
		for k in range(5):
			maxi = 0
			actual = 0
			for j in range(1000,4047):
				if j==five[0] or j==five[1] or j==five[2] or j==five[3] or j==five[4]:
					continue
				if maxi < sim[j]:
					maxi = sim[j]
					actual = number[j]
			if five[0] == 0:
				five[0]=actual
			elif five[1] == 0:
				five[1] = actual
			elif five[2] == 0:
				five[2] = actual
			elif five[3] == 0:
				five[3] = actual
			elif five[4] == 0:
				five[4] = actual
		total_cases = recommender[five[0]].cases + recommender[five[1]].cases + recommender[five[2]].cases + recommender[five[3]].cases + recommender[five[4]].cases
		recommender[number[i]].prediction = (recommender[five[0]].prob * recommender[five[0]].cases+ 
										recommender[five[1]].prob * recommender[five[1]].cases+
										recommender[five[2]].prob * recommender[five[2]].cases+
										recommender[five[3]].prob * recommender[five[3]].cases+
										recommender[five[4]].prob * recommender[five[4]].cases)/total_cases

def MAE(recommender, number):
	total = 0
	for i in range(1000):
		total = total + abs(recommender[number[i]].prediction - recommender[number[i]].prob)
	return total/1000

def RMSE(recommender, number):
	total = 0
	for i in range(1000):
		total = total + pow((recommender[number[i]].prediction - recommender[number[i]].prob),2)
	return (total/1000)**0.5




