import cplex
import getopt
import math
import numpy as np
import os
import psycopg2
import random
import sys
import time

def ReadInput():
	global input_file_path
	global connections
	global size_dic
	global max_degree

	size_dic = {}
	id_dic = {}
	id_num = 0

	connections = []

	input_file = open(input_file_path,'r')

	for line in input_file.readlines():
		elements = line.split()
		connection = []

		for element in elements[1 : ]:
			element = int(element)

			if element in id_dic.keys():
				element = id_dic[element]
			else:
				id_dic[element] = id_num
				element = id_num
				id_num += 1

			if element in size_dic.keys():
				size_dic[element] += 1
			else:
				size_dic[element] = 1

			connection.append(element)

		connections.append(connection)

	max_degree = max(size_dic.values())

def RestrictedSensitivity():
	global theta
	global k

	if k == 0:		# edge
		return theta
	elif k == 1:	# triangle
		return theta * (theta - 1) / 2
	elif k == 2:	# two path
		return theta * (theta - 1) * 3 / 2
	elif k == 3:	# rectangle
		return theta * (theta - 1) * (theta - 1) / 2
	else:
		return 0

def LocalSensitivity(i):
	global theta
	global size_dic

	count = 0

	for val in size_dic.values():
		if val >= theta - i and val <= theta + i + 1:
			count += 1

	return count

def CauchyCum(x):
	a = 1/4/math.sqrt(2)*(math.log(abs(x**2+math.sqrt(2)*x+1))+2*math.atan(math.sqrt(2)*x+1))
	a += 1/4/math.sqrt(2)*(-math.log(abs(x**2-math.sqrt(2)*x+1))+2*math.atan(math.sqrt(2)*x-1))

	return a

def CauNoise():
	a = random.uniform(0,math.pi/2/math.sqrt(2))

	left = 0
	right = 6000
	mid = (left + right) / 2.0

	while(abs(CauchyCum(mid) - a) > 0.000001):
		if CauchyCum(mid) > a:
			right = mid
		else:
			left = mid
		mid = (left + right) / 2.0

	c = random.uniform(0, 1)

	if c > 0.5:
		return mid
	else:
		return -mid

def Truncation():
	global theta
	global connections
	global size_dic
	global connections_truncated
	global output_file_path
	global k

	connections_truncated = []

	for connection in connections:
		if size_dic[connection[0]] <= theta and size_dic[connection[1]] <= theta:
			connections_truncated.append(connection)

	output_file_path = input_file_path[ : input_file_path.rfind('/')] + "/../../../Temp/nt_" + input_file_path[input_file_path.rfind('/') + 1 : ] + "_" + str(theta) + ".txt"
	output_file = open(output_file_path,'w')

	for connection in connections_truncated:
		output_file.write(str(connection[0]) + ' ' + str(connection[1]) + '\n')
		output_file.write(str(connection[1]) + ' ' + str(connection[0]) + '\n')

def Count():
	global k
	global connections_truncated
	global output_file_path
	global database_name
	global real_ans

	con = psycopg2.connect(dbname=database_name)
	cur = con.cursor()

	output_file = open(output_file_path, 'r')

	cur.execute("CREATE TABLE EDGE (FROM_ID INTEGER NOT NULL, TO_ID INTEGER NOT NULL);")
	cur.execute("CREATE INDEX on EDGE using hash (FROM_ID);")
	cur.execute("CREATE INDEX on EDGE using hash (TO_ID);")

	cur.copy_from(output_file, 'EDGE', sep=' ')

	num = 0
	query = ""

	if k == 0:		# edge
		query = "SELECT count(*) FROM edge WHERE edge.from_id < edge.to_id;"
	elif k == 1:	# triangle
		query = "SELECT count(*) FROM edge as r4, edge as r5, edge as r6 WHERE r4.from_id = r6.to_id and r5.from_id = r4.to_id and r6.from_id = r5.to_id and r4.from_id < r5.from_id and r5.from_id < r6.from_id;"
	elif k == 2:	# two path
		query = "SELECT count(*) FROM edge as r4, edge as r5 WHERE r5.from_id = r4.to_id and r4.from_id < r5.to_id;"
	elif k == 3:	# rectangle
		query = "SELECT count(*) FROM edge as r5, edge as r6, edge as r7, edge as r8 WHERE r5.from_id = r8.to_id and r6.from_id = r5.to_id and r7.from_id = r6.to_id and r8.from_id = r7.to_id and r5.from_id < r6.from_id and r5.from_id < r7.from_id and r5.from_id < r8.from_id and r6.from_id < r8.from_id;"
	else:
		con.commit()
		con.close()

		real_ans = num

		return real_ans

	cur.execute(query)

	num = int(cur.fetchall()[0][0])

	cur.execute("DROP TABLE EDGE;")

	con.commit()
	con.close()

	os.remove(output_file_path)

	real_ans = num

	return real_ans

def RunAlgorithm():
	global epsilon
	global theta
	global max_degree
	global ss

	Truncation()

	base = math.e
	beta = epsilon / 10

	max_ss_truncation = 0
	
	for i in range(max(max_degree, theta)):
		ls_truncation = LocalSensitivity(i) + i + 1
		ss_truncation = math.pow(base, - beta * i) * ls_truncation
		if ss_truncation > max_ss_truncation:
			max_ss_truncation = ss_truncation

	ss = max_ss_truncation * RestrictedSensitivity()

	return Count() + CauNoise() * 10 * ss / epsilon

def main(argv):
	global input_file_path
	global epsilon
	global theta
	global k
	global database_name
	global real_ans
	global ss
	
	try:
		opts, args = getopt.getopt(argv,"h:I:e:t:k:D:",["Input=","epsilon=","theta=","k=","D="])
	except getopt.GetoptError:
		print("NT.py -I <input file> -e <epsilon> -t <theta> -k <k> -D <database>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("NT.py -I <input file> -e <epsilon> -t <theta> -k <k> -D <database>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_file_path = str(arg)
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg)
		elif opt in ("-t","--theta"):
			theta = int(arg)
		elif opt in ("-k","--k"):
			k = int(arg)
		elif opt in ("-D","--Database"):
			database_name = str(arg)

	start = time.time()

	ReadInput()

	res = RunAlgorithm()

	end= time.time()

	print("Query Result")
	print(real_ans)
	print("Smooth Sensitivity")
	print(ss)
	print("Time")
	print(end - start)

if __name__ == "__main__":
	main(sys.argv[1:])
