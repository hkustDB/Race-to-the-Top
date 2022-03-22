import getopt
import psycopg2
import sys

def ReadQuery():
    global query
    global query_path

    query = ""
    query_file = open(query_path,'r')

    # Read the query file and store in query
    for line in query_file.readlines():
        query = query + line
        if ";" in query:
            query = query.replace('\n'," ")
            break

def ReadPrimaryKey():
    global primary_key_list
    global primary_key_path

    # Read and store the primary key(s) of the private relation
    key_list_file = open(primary_key_path,'r')
    line = key_list_file.readline()
    primary_key_list = line.split()

def RewriteQuery():
    global query
    global private_relation_name
    global rewrite_query
    global primary_key_list
    global renaming_private_relations

    # Split the query into select, from and where clauses
    #Match the corresponding terms
    from_string = ""
    select_string = ""
    where_string = ""
    query_t = query.replace(","," ")
    words = query_t.split(" ")

    for word in words:
        if word.lower() == "select":
            select_string = word
        if word.lower() == "from":
            from_string = word
        if word.lower() == "where":
            where_string = word

    parser_string = query
    parser_string = parser_string.replace(select_string + " ", "")
    parser_string = parser_string.replace(from_string + " ", "\n")
    parser_string = parser_string.replace(where_string + " ", "\n")
    parser_string = parser_string.replace(";", "")
    parser_strings = parser_string.split("\n")

    select_strings = parser_strings[0]
    from_strings = parser_strings[1]
    where_strings = parser_strings[2]

    # Split the select attributes
    select_strings = select_strings.replace(",", "\n")
    select_strings = select_strings.split("\n")

    # Split the relations
    relations_strings = from_strings.replace(",", "\n")
    relations_strings = relations_strings.split("\n")

    # Renaming_private_relations stores all the relations that are private
    renaming_private_relations = []

    # Go through the relations in the from clause
    for relations_string in relations_strings:
        relations_string = relations_string.split()
        origin_relation = relations_string[0]

        # Case 1: there is a renaming, xxx as xxx
        if len(relations_string) > 1:
            renaming_relation = relations_string[2]
        # Case 2: there is no renaming
        else:
            renaming_relation = relations_string[0]

        # Append the private relations to the list
        if origin_relation == private_relation_name:
            renaming_private_relations.append(renaming_relation)

    # Rewrite the query
    rewrite_query = "select "
    # Case 1: aggregation query
    if "sum" in select_strings[0]:
        if " as " in select_strings[0]:
            select_strings[0] = select_strings[0].replace(" as ", "\n").split("\n")[0]

        rewrite_query = rewrite_query + select_strings[0][select_strings[0].find('(') + 1 : select_strings[0].rfind(')')] + ", "
    # Case 2: counting query
    else: 
        rewrite_query = rewrite_query + "1, "

    # Go through all the private relations
    for i in range(len(renaming_private_relations)):
        concat_attr = ""

        # Concatenate all the private key(s) as the attribbute
        for j in range(len(primary_key_list)):
            if j == 0:
                concat_attr = "concat(" + renaming_private_relations[i] + "." + primary_key_list[j] + ",\',\')"
            else:
                concat_attr = concat_attr + "||concat(" + renaming_private_relations[i] + "." + primary_key_list[j] + ",\',\')"
        
        concat_attr = concat_attr + " as id" + str(i)

        # Add the private relation to select clause
        if i == 0:
            rewrite_query = rewrite_query + concat_attr
        else:
            rewrite_query = rewrite_query + ", " + concat_attr

    # Combine all the parts of the rewrite query
    rewrite_query = rewrite_query + " from " + from_strings + " where " + where_strings + ";"

def ExtractRelationship():
    global database_name
    global rewrite_query
    global output_file
    global renaming_private_relations

    con = psycopg2.connect(database=database_name)
    cur = con.cursor()

    # Run the query and get the results
    cur.execute(rewrite_query)
    res = cur.fetchall()

    id_dic = {}
    results = open(output_file, 'w')
    num_id = 0

    # Go through the results
    for i in range(len(res)):
        temp_res = res[i]
        # Write the count/aggregation result
        results.write(str(temp_res[0]) + " ")

        # Write the private relations in the result
        for j in range(1, len(renaming_private_relations) + 1):
            temp_id = temp_res[j]

            # Reordering the private relations
            if temp_id in id_dic:
                results.write(str(id_dic[temp_id]) + " ")
            else:
                id_dic[temp_id] = num_id
                results.write(str(num_id) + " ")
                num_id += 1

        results.write("\n")

    con.commit()
    con.close()

def main(argv):
    # Name of the database to be queried
    global database_name
    # Path of the txt file storing the query
    global query_path
    # Name of the private relation
    global private_relation_name
    # Path of the txt file storing the primary key(s) of the private relation
    global primary_key_path
    # Path of the output file of the query results
    global output_file

    try:
        opts, args = getopt.getopt(argv,"h:D:Q:P:K:O:",["Database=","QueryPath=","PrivateRelationName=","PrimaryKey=","Output="])
    except getopt.GetoptError:
        print("ExtractInfo.py -D <database name> -Q <query file path> -P <private relation name> -K <primary key of private relation> -O <output file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("ExtractInfo.py -D <database name> -Q <query file path> -P <private relation name> -K <primary key of private relation> -O <output file>")
            sys.exit()
        elif opt in ("-D", "--Database"):
            database_name = arg
        elif opt in ("-Q","--QueryPath"):
            query_path = arg
        elif opt in ("-P","--PrivateRelationName"):
            private_relation_name = arg
        elif opt in ("-K","--PrimaryKey"):
            primary_key_path=arg
        elif opt in ("-O","--Output"):
            output_file=arg

    ReadQuery()
    ReadPrimaryKey()
    RewriteQuery()
    ExtractRelationship()
    
if __name__ == "__main__":
   main(sys.argv[1:])