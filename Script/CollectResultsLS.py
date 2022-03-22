import math
import os
import sys

repeat_times = 30

epsilons = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
queries = [("Q3", 2888656), ("Q12", 6001215), ("Q20", 6001215)]
scales = ["_3"]

GS = 1000000.0

def main(argv):
	for (query, real_ans) in queries:
		cur_path = os.getcwd()

		output_file = open(cur_path + "/../Result/TPCH/LS_" + query + ".txt", 'w')

		for scale in scales:
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "python " + cur_path + "/../Code/LS.py -I " + cur_path + "/../Information/TPCH/" + query + scale + ".txt -e " + str(epsilon) + " -G " + str(int(GS))

				for i in range(repeat_times):
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					a = float(res[2])
					b = float(res[5])
					c = float(res[7])
		
					errors.append(abs(a - b))
					sum_time += c

				errors.sort()

				output_file.write(str(epsilon) + " " + str(real_ans) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum_time/repeat_times) + "\n")

if __name__ == "__main__":
	main(sys.argv[1:])