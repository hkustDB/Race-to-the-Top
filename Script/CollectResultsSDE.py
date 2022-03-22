import getopt
import math
import os
import random
import sys
import time

repeat_times = 10
trials = 1000

epsilons = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
graphs = ["Amazon2", "Amazon1", "RoadnetPA", "RoadnetCA", "Deezer"]
ks = ["one_path", "triangle", "two_path", "rectangle"]

def RestrictedSensitivity(theta, k):
	theta_ = 2 * theta

	if k == 0:		# edge
		return theta_
	elif k == 1:	# triangle
		return theta_ * (theta_ - 1) / 2
	elif k == 2:	# rectangle
		return theta_ * (theta_ - 1) * (theta_ - 1) / 2
	elif k == 3:	# two triangle
		return theta_ * (theta_ - 1) * (theta_ - 2)
	elif k == 4:	# two path
		return theta_ * (theta_ - 1) * 3 / 2
	else:
		return 0

def SS(distance_estimator, epsilon, theta, k):
	base = math.e
	beta = epsilon / 10

	round_distance_estimator = math.ceil(distance_estimator)
	s_max = math.pow(base, - beta / 4 * (round_distance_estimator - distance_estimator)) * (2 * round_distance_estimator + 5) * RestrictedSensitivity(theta, k)

	d_1 = math.floor(4 / beta - 5 / 2)
	d_2 = math.ceil(4 / beta - 5 / 2)

	if d_1 >= distance_estimator:
		s = math.pow(base, - beta / 4 * (d_1 - distance_estimator)) * (2 * d_1 + 5) * RestrictedSensitivity(theta, k)
		if s > s_max:
			s_max = s
	
	if d_2 >= distance_estimator:
		s = math.pow(base, - beta / 4 * (d_2 - distance_estimator)) * (2 * d_2 + 5) * RestrictedSensitivity(theta, k)
		if s > s_max:
			s_max = s

	return s_max

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
		print("CollectResultsSDE.py -G <graph> -Q <query> -e <epsilon>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("CollectResultsSDE.py -G <graph> -Q <query> -e <epsilon>")
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

	lp_time_dict = {}
	count_time_dict = {}
	error_time_dict = {}

	dist_dict = {}
	count_dict = {}
	ss_dict = {}
	
	cur_path = os.getcwd()

	for graph in graphs:
		if graph == "Amazon2":
			thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0]
			lp_thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0]
			fail_thetas = []
			max_theta = 1024.0
			min_theta = 2.0
		elif graph == "Amazon1":
			thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0]
			lp_thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0]
			fail_thetas = [4.0, 2.0]
			max_theta = 1024.0
			min_theta = 8.0
		elif graph == "Deezer":
			thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0]
			lp_thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0]
			fail_thetas = [16.0, 8.0, 4.0, 2.0]
			max_theta = 1024.0
			min_theta = 32.0
		else:
			thetas = [16.0, 8.0, 4.0, 2.0]
			lp_thetas = [16.0, 8.0, 4.0, 2.0]
			fail_thetas = []
			max_theta = 16.0
			min_theta = 2.0

		for theta in lp_thetas:
			cmd = "python " + cur_path + "/../Code/SDE.py -I " + cur_path + "/../Information/Graph/one_path/" + graph + ".txt -e 0.8 -t " + str(int(theta)) + " -k 0 -D SDE_" + graph + " -m 1"

			shell = os.popen(cmd, 'r')
			res = shell.read()
			res = res.split()

			distance_estimator = float(res[2])
			time_ = float(res[4])

			dist_dict[(graph, theta)] = distance_estimator
			lp_time_dict[(graph, theta)] = time_

			for i in range(len(ks)):
				query = ks[i]

				cmd = "python " + cur_path + "/../Code/SDE.py -I " + cur_path + "/../Information/Graph/one_path/" + graph + ".txt -e 0.8 -t " + str(int(theta)) + " -k 0 -D SDE_" + graph + " -m 2"
				
				sum_time = 0

				for j in range(repeat_times):
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					count = int(float(res[1]))
					time_ = float(res[3])

					count_dict[(graph, theta, query)] = count
					sum_time += time_
				
				count_time_dict[(graph, theta, query)] = sum_time / repeat_times

				for epsilon in epsilons:
					sum_time = 0

					for j in range(repeat_times):
						start = time.time()

						ss_dict[(graph, theta, query, epsilon)] = SS(dist_dict[(graph, theta)], epsilon, theta, i)
						result = count_dict[(graph, theta, query)] + CauNoise() * 10 * ss_dict[(graph, theta, query, epsilon)] / epsilon

						end = time.time()

						sum_time += end - start

					error_time_dict[(graph, theta, query, epsilon)] = sum_time / repeat_times

		time_dict = {}
					
		for i in range(len(ks)):
			query = ks[i]

			output_file = open(cur_path + "/../Result/Graph/SDE_" + query + "_" + graph + ".txt", 'w')

			for epsilon in epsilons:
				for theta in lp_thetas:
					time_dict[(graph, theta, query, epsilon)] = lp_time_dict[(graph, theta)] + count_time_dict[(graph, theta, query)] + error_time_dict[(graph, theta, query, epsilon)]

				for theta in fail_thetas:
					time_dict[(graph, theta, query, epsilon)] = 21600.0

				errors = []
				count_fail = 0

				for j in range(trials):
					random_theta = random.choice(thetas)

					if random_theta < min_theta:
						count_fail += 1
						real_count = count_dict[(graph, max_theta, query)]

						errors.append(1e20)
					else:
						result = count_dict[(graph, random_theta, query)] + CauNoise() * 10 * ss_dict[(graph, random_theta, query, epsilon)] / epsilon
						real_count = count_dict[(graph, max_theta, query)]

						error = abs(result - real_count)
						errors.append(error)

				errors.sort()

				sum_time = 0

				for theta in thetas:
					sum_time += time_dict[(graph, theta, query, epsilon)]

				average_time = sum_time / len(thetas)

				if count_fail < int(float(trials * 0.2)):
					output_file.write(str(epsilon) + " " + str(real_count) + " " + str(sum(errors[int(float(trials * 0.2)) : trials - int(float(trials * 0.2))]) / int(float(trials * 0.6))) + " " + str(average_time) + "\n")
				else:
					output_file.write(str(epsilon) + " " + str(real_count) + " " + str(sum(errors[count_fail: trials - count_fail]) / (trials - 2 * count_fail)) + " " + str(average_time) + "\n")

if __name__ == "__main__":
	main(sys.argv[1:])