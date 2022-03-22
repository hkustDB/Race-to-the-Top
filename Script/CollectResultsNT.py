import getopt
import math
import os
import random
import sys

repeat_times = 10
trials = 1000

epsilons = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
graphs = ["Amazon2", "Amazon1", "RoadnetPA", "RoadnetCA", "Deezer"]
ks = ["one_path", "triangle", "two_path", "rectangle"]

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

def main(argv):
	global repeat_times
	global trials
	global epsilons
	global graphs
	global ks

	try:
		opts, args = getopt.getopt(argv,"h:G:Q:e:",["Graph=","Query=","epsilon="])
	except getopt.GetoptError:
		print("CollectResultsNT.py -G <graph> -Q <query> -e <epsilon>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("CollectResultsNT.py -G <graph> -Q <query> -e <epsilon>")
			sys.exit()
		elif opt in ("-G", "--Graph"):
			if str(arg) in graphs:
				graphs = [str(arg)]
		elif opt in ("-Q", "--Query"):
			if str(arg) in ks:
				ks = [str(arg)]
		elif opt in ("-e", "--epsilon"):
			if float(arg) in epsilons:
				epsilons = [float(arg)]

	count_dict = {}
	ss_dict = {}
	time_dict = {}

	cur_path = os.getcwd()

	for graph in graphs:
		if graph == "Amazon2" or graph == "Amazon1" or graph == "Deezer":
			thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0]
			max_theta = 1024.0
		else:
			thetas = [16.0, 8.0, 4.0, 2.0]
			max_theta = 16.0

		for i in range(len(ks)):
			query = ks[i]

			output_file = open(cur_path + "/../Result/Graph/NT_" + query + "_" + graph + ".txt", 'w')

			for epsilon in epsilons:
				for theta in thetas:
					sum_time = 0

					cmd = "python " + cur_path + "/../Code/NT.py -I " + cur_path + "/../Information/Graph/one_path/" + graph + ".txt -e " + str(epsilon) + " -t " + str(int(theta)) + " -k " + str(i) + " -D NT_" + graph

					for j in range(repeat_times):
						shell = os.popen(cmd, 'r')
						res = shell.read()
						res = res.split()

						time = float(res[7])

						if j == 0:
							count = int(float(res[2]))
							ss = float(res[5])

							count_dict[(graph, query, theta)] = count
							ss_dict[(graph, query, epsilon, theta)] = ss

						sum_time += time

					average_time = sum_time / repeat_times

					time_dict[(graph, query, epsilon, theta)] = average_time

				errors = []

				for j in range(trials):
					random_theta = random.choice(thetas)

					result = count_dict[(graph, query, random_theta)] + CauNoise() * 10 * ss_dict[(graph, query, epsilon, random_theta)] / epsilon
					real_count = count_dict[(graph, query, max_theta)]

					error = abs(result - real_count)
					errors.append(error)

				errors.sort()

				sum_time = 0

				for theta in thetas:
					sum_time += time_dict[(graph, query, epsilon, theta)]

				average_time = sum_time / len(thetas)

				output_file.write(str(epsilon) + " " + str(real_count) + " " + str(sum(errors[int(float(trials * 0.2)) : trials - int(float(trials * 0.2))]) / int(float(trials * 0.6))) + " " + str(average_time) + "\n")
				
if __name__ == "__main__":
	main(sys.argv[1:])