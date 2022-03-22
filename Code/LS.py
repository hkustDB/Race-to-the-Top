import cplex
import getopt
import math
import numpy as np
import psycopg2
import random
import sys
import time

def ReadInput():
	global input_file_path
	global size_dic
	global real_ans
	global max_degree

	size_dic = {}
	tuples = []

	input_file = open(input_file_path,'r')

	for line in input_file.readlines():
		elements = line.split()
		primary_id = int(elements[1])

		if primary_id in size_dic.keys():
			size_dic[primary_id] += 1
		else:
			size_dic[primary_id] = 1

	real_ans = sum(size_dic.values())
	max_degree = max(size_dic.values())

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def QueryCount(i):
	global size_dic
	global real_ans
	global max_degree

	if i >= max_degree:
		return real_ans

	size_dic_i = dict((k, v) for k, v in size_dic.items() if v <= i)

	return sum(size_dic_i.values())

def Svt():
	global epsilon_q_l
	global epsilon_svt
	global l

	q_l = QueryCount(l)
	q_hat_l = q_l + LapNoise() * l / epsilon_q_l

	t = 0
	t_hat = t + LapNoise() * 2 / epsilon_svt

	for i in range(1, l):
		q_i = QueryCount(i)
		v_i = LapNoise() * 4 / epsilon_svt

		if (q_i - q_hat_l) / i + v_i >= t_hat:
			return q_i, i
	
	return q_l, l

def RunAlgorithm():
	global epsilon_ans

	ans, tau = Svt()

	return ans + LapNoise() * tau / epsilon_ans

def main(argv):
	global input_file_path
	global epsilon_q_l
	global epsilon_svt
	global epsilon_ans
	global l
	global real_ans
	
	try:
		opts, args = getopt.getopt(argv,"h:I:e:G:",["Input=","epsilon=","GS="])
	except getopt.GetoptError:
		print("LS.py -I <input file> -e <epsilon> -G <GS>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("LS.py -I <input file> -e <epsilon> -G <GS>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_file_path = str(arg)
		elif opt in ("-e","--epsilon"):
			epsilon_q_l = float(arg) * 0.25
			epsilon_svt = float(arg) * 0.25
			epsilon_ans = float(arg) * 0.5
		elif opt in ("-G","--GS"):
			l = int(arg)

	start = time.time()

	ReadInput()

	res = RunAlgorithm()

	end= time.time()

	print("Query Result")
	print(real_ans)
	print("Noised Result")
	print(res)
	print("Time")
	print(end - start)

if __name__ == "__main__":
	main(sys.argv[1:])
