import os
import psycopg2
import sys
import time

repeat_times = 10
queries = ["one_path", "triangle", "two_path", "rectangle"]
databases = ["Amazon2", "Amazon1", "RoadnetPA", "RoadnetCA", "Deezer"]

def ExtractRelationship(database_name, query):
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()

    cur.execute(query)

    con.commit()
    con.close()

def main(argv):
	cur_path = os.getcwd()

	output_file = open(cur_path + "/../Result/Graph/QueryTimeGraph.txt", 'w')

	for database_name in databases:
		for query_type in range(len(queries)):
			query_name = queries[query_type]
			sum_time = 0

			for j in range(repeat_times):
				start = time.time()

				if query_type == 0:
					query = "select 1, r1.id, r2.id from node as r1, node as r2, edge where r1.id=edge.from_id and r2.id=edge.to_id and r1.id<r2.id;"
				elif query_type == 1:
					query = "select 1, r1.id, r2.id, r3.id from node as r1, node as r2, node as r3, edge as r4, edge as r5, edge as r6 where r4.from_id = r6.to_id and r5.from_id = r4.to_id and r6.from_id = r5.to_id and r1.id = r4.from_id and r2.id = r5.from_id and r3.id = r6.from_id and r1.id<r2.id and r2.id<r3.id;"
				elif query_type == 2:
					query = "select 1, r1.id, r2.id, r3.id from node as r1, node as r2, node as r3, edge as r4, edge as r5 where r4.to_id = r5.from_id and r1.id = r4.from_id and r2.id = r5.from_id and r3.id = r5.to_id and r1.id < r3.id;"
				elif query_type == 3:
					query = "select 1, r1.id, r2.id, r3.id, r4.id from node as r1, node as r2, node as r3, node as r4, edge as r5, edge as r6, edge as r7, edge as r8 where r5.from_id = r8.to_id and r6.from_id = r5.to_id and r7.from_id = r6.to_id and r8.from_id = r7.to_id and r1.id = r5.from_id and r2.id = r6.from_id and r3.id = r7.from_id and r4.id = r8.from_id and r1.id < r2.id and r1.id < r3.id and r1.id < r4.id and r2.id < r4.id;"

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " " + query_name + " " + str(sum_time/repeat_times) + "\n")

if __name__ == "__main__":
	main(sys.argv[1:])