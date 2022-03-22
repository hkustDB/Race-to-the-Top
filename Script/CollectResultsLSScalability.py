import math
import os
import sys

repeat_times = 30

epsilons = [0.8]
queries = ["Q3", "Q12", "Q20"]
scales = ["_0", "_1", "_2", "_3", "_4", "_5", "_6"]

GS = 1000000.0

def main(argv):
	for query in queries:
		cur_path = os.getcwd()

		output_file = open(cur_path + "/../Result/TPCH/LS_" + query + "_Scalability.txt", 'w')

		for l_scale in range(len(scales)):
			scale = scales[l_scale]

			for epsilon in epsilons:
				real_ans = 0
				sum_time = 0
				errors = []

				cur_path = os.getcwd()
				cmd = "python " + cur_path + "/../Code/LS.py -I " + cur_path + "/../Information/TPCH/" + query + scale + ".txt -e " + str(epsilon) + " -G " + str(int(GS))

				for i in range(repeat_times):
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					a = float(res[2])
					b = float(res[5])
					c = float(res[7])
		
					real_ans = int(a)
					errors.append(abs(a - b))
					sum_time += c

				errors.sort()

				output_file.write(str(math.pow(2, l_scale - 3)) + " " + str(real_ans) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum_time/repeat_times) + "\n")

if __name__ == "__main__":
	main(sys.argv[1:])