import os
import sys
import time

repeat_times = 10
queries = ["one_path", "triangle", "two_path", "rectangle"]
databases = ["Amazon2", "Amazon1", "RoadnetPA", "RoadnetCA", "Deezer"]

def main(argv):
	cur_path = os.getcwd()

	output_file = open(cur_path + "/../Result/Graph/ExtractInfoTimeGraph.txt", 'w')

	for database in databases:
		for query in queries:
			sum_time = 0

			for i in range(repeat_times):
				start = time.time()

				cmd = "python " + cur_path + "/../Code/ExtractInfo.py -D " + database + " -Q " + cur_path + "/../Query/" + query + ".txt -K " + cur_path + "/../Query/" + query + "_key.txt -P node -O " + cur_path + "/../Temp/aaa.txt"
				
				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()
				
				end = time.time()

				sum_time += end - start

			output_file.write(database + " " + query + " " + str(sum_time/repeat_times) + "\n")

	os.remove(cur_path + "/../Temp/aaa.txt")

if __name__ == "__main__":
	main(sys.argv[1:])