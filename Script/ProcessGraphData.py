import getopt
import psycopg2
import os
import sys

def main(argv):
	datasets = ["Amazon1", "Amazon2", "RoadnetPA", "RoadnetCA", "Deezer"]
	dataset = ''
	database_name = ''
	model = 0

	try:
		opts, args = getopt.getopt(argv,"h:d:D:m:",["dataset=","database=","model="])
	except getopt.GetoptError:
		print("ProcessGraphData.py -d <dataset> -D <database> -m <model:0(import)/1(clean)>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ProcessGraphData.py -d <dataset> -D <database> -m <model:0(import)/1(clean)>")
			sys.exit()
		elif opt in ("-d", "--dataset"):
			dataset = arg
		elif opt in ("-D", "--Database"):
			database_name = arg
		elif opt in ("-m","--model"):
			model = int(arg)

	if model==0:
		if dataset not in datasets:
			print("Invalid dataset.")
			sys.exit()

		con = psycopg2.connect(database=database_name)
		cur = con.cursor()

		cur_path = os.getcwd()

		edge_file = open(cur_path+"/../Data/Graph/"+dataset+"_edges.txt", 'r')
		node_file = open(cur_path+"/../Data/Graph/"+dataset+"_nodes.txt", 'r')

		code = "CREATE TABLE NODE (ID INTEGER NOT NULL);"
		cur.execute(code)
		code = "CREATE TABLE EDGE (FROM_ID INTEGER NOT NULL, TO_ID INTEGER NOT NULL);"
		cur.execute(code)
		code = "CREATE INDEX on NODE using hash (ID);"
		cur.execute(code)
		code = "CREATE INDEX on EDGE using hash (FROM_ID);"
		cur.execute(code)
		code = "CREATE INDEX on EDGE using hash (TO_ID);"
		cur.execute(code)

		cur.copy_from(edge_file, 'EDGE', sep='|')
		cur.copy_from(node_file, 'NODE')

		con.commit()
		con.close()
	else:
		con = psycopg2.connect(database=database_name)
		cur = con.cursor()

		code = "drop table node;"
		cur.execute(code)
		code = "drop table edge;"
		cur.execute(code)

		con.commit()
		con.close()

if __name__ == "__main__":
   main(sys.argv[1:])