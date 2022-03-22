import math
import os
import sys

repeat_times = 10

epsilons = [0.8]
queries = ["Q3", "Q12", "Q20"]
scale = "_3"

def main(argv):
	GS = 10000.0

	for query in queries:
		cur_path = os.getcwd()

		output_file = open(cur_path + "/../Result/TPCH/LS_" + query + "_GS.txt", 'w')

		for pow_ in range(8):
			for epsilon in epsilons:
				errors = []

				cmd = "python " + cur_path + "/../Code/LS.py -I " + cur_path + "/../Information/TPCH/" + query + scale + ".txt -e " + str(epsilon) + " -G " + str(int(GS))

				for i in range(repeat_times):
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					a = float(res[2])
					b = float(res[5])
		
					errors.append(abs(a - b))

				errors.sort()

				output_file.write(str(GS) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")

			GS *= 10

if __name__ == "__main__":
	main(sys.argv[1:])