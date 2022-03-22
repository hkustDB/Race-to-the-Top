import getopt
import os
import sys

def main(argv):
    # Name of the database to be queried
    global database_name
    # Path of the txt file storing the query
    global query_path
    # Name of the private relation
    global private_relation_path
    # Path of the txt file storing the primary key(s) of the private relation
    global primary_key_path
    #Privacy budget
    global epsilon
    epsilon = 0.1
    #Error probablity: with probablity at least 1-beta, the error can be bounded
    global beta
    beta = 0.1
    #The global sensitivity
    global global_sensitivity
    global_sensitivity = 1000000
    #The number of processor
    global processor_num
    processor_num = 10
    try:
        opts, args = getopt.getopt(argv,"h:D:Q:P:K:e:b:G:p:",["Database=","QueryPath=","PrivateRelationPath=","PrimaryKey=","epsilon=","beta=","GlobalSensitivity=","ProcessorNum="])
    except getopt.GetoptError:
        print("System.py -D <database name> -Q <query file path> -P <private relation path> -K <primary key of private relation> -e <epsilon(default 0.1)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("System.py -D <database name> -Q <query file path> -P <private relation path> -K <primary key of private relation> -e <epsilon(default 0.1)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)>")
            sys.exit()
        elif opt in ("-D", "--Database"):
            database_name = arg
        elif opt in ("-Q","--QueryPath"):
            query_path = arg
        elif opt in ("-P","--PrivateRelationName"):
            private_relation_path = arg
        elif opt in ("-K","--PrimaryKey"):
            primary_key_path=arg
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b","--beta"):
            beta = float(arg)
        elif opt in ("-G","--GlobalSensitivity"):
            global_sensitivity = float(arg)
        elif opt in ("-p","--ProcessorNum"):
            processor_num = int(arg)
    #Extract Relationship between base tables' tuples     
    cur_path=os.getcwd()
    cmd = "python "+cur_path+"/../Code/SystemExtractInfo.py -D "+database_name+" -Q "+query_path
    cmd = cmd+" -P "+private_relation_path+" -K "+primary_key_path+" -O "+cur_path+"/../Temp/TempInfo.txt"
    shell = os.popen(cmd, 'r')
    shell.read()
    shell.close()
    # Run R2T
    cmd = "python "+cur_path+"/../Code/R2T.py -I "+cur_path+"/../Temp/TempInfo.txt"
    cmd = cmd+" -b"+str(beta)+" -e "+str(epsilon)+" -G "+str(global_sensitivity)+" -p "+str(processor_num)
    shell = os.popen(cmd, 'r')
    res = shell.read()
    res = res.split()
    print("Noised Result")
    print(res[5])
    shell.close()
    # Delete the temp file
    cmd = "rm "+cur_path+"/../Temp/TempInfo.txt"
    shell = os.popen(cmd, 'r')
    shell.read()
    shell.close()
    
    

if __name__ == "__main__":
   main(sys.argv[1:])