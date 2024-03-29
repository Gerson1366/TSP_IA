'''
Developer: Francisco Nascimento, adapted from Abhishek Manoj Sharma
Course: Artificial Intelligence 2019/2
Date: August 25, 2019
'''

from argparse import ArgumentParser
import time
import os.path
from math import sin, cos, sqrt, atan2, radians

# ---------------------------------------------------------------------------------------------------
# Define the start node of the travel, which should be also the final one
TOUR_START_NODE_INDEX = 0
total_tour_length = 0
visited = []
visited_nodes = []

# ---------------------------------------------------------------------------------------------------
# readTSPFile() method to read TSP file and to produce distance matrix with costs
# ---------------------------------------------------------------------------------------------------
def readTSPFile(tsp_file_name):
    number_of_nodes = 0;
    costs = {}
    with open(tsp_file_name) as tsp_file:
        for line in tsp_file:
            if "DIMENSION" in line:
                splittedLine = line.strip().split(":")
                number_of_nodes = int(splittedLine[1])
            if "EDGE_WEIGHT_TYPE" in line:
                splittedLine = line.strip().split(":")
            if "EDGE_WEIGHT_SECTION" in line:
                i = 0;
                for line in tsp_file:
                    if not (line.strip() == "EOF"):
                        splittedLine = line.strip().split()
                        for j in range(i+1,len(splittedLine)+i+1):
                            #costs.append( ( i,j,float(splittedLine[j-i-1]) ) );
                            costs[i,j] = float(splittedLine[j-i-1]);
                            #print(i,j,splittedLine[j-i-1]);
                    i=i+1;
            if "NODE_COORD_SECTION" in line:
                i = 0;
                coordenada_x = []
                coordenada_y = []
                #percorre as linhas e joga as coordenadas x e y em duas listas para cada coordenada
                for line in tsp_file:
                    if not (line.strip() == "EOF"):
                        splittedLine = line.strip().split()
                        coordenada_x.append(float(splittedLine[1]))
                        coordenada_y.append(float(splittedLine[2]))
                        #print("x",float(splittedLine[1]),"y",float(splittedLine[2]))
                i = 0
                j = 0
                #Compara cidade com cidade anterior, construindo matriz diagonal superior
                for i in range(i,len(coordenada_x)):
                    for j in range(j,len(coordenada_x)):
                        #calcula distancia com distancia euclidiana
                        lat1 = radians(coordenada_x[i])
                        lon1 = radians(coordenada_y[i])
                        lat2 = radians(coordenada_x[j])
                        lon2 = radians(coordenada_y[j])
                        dlon = (lon2 - lon1)**2
                        dlat = (lat2 - lat1)**2
                        a = dlat+dlon
                        #c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distance = sqrt(a)
                        #Ignora distancia da cidade para si mesma
                        #if(i!=j):
                        costs[i,j] = distance*1000
                        j=0
                            #print(i,",",j,":",costs[i,j])
                        #print(i,j,splittedLine[j-i-1]);
    return number_of_nodes,costs

# ---------------------------------------------------------------------------------------------------
# greedy_main_run() method drives the program by calling the readTSPFile() method to produce
#   distance matrix and then the computePathGreedy() method to calculate path using Greedy algorithm
# ---------------------------------------------------------------------------------------------------
def greedy_main_run(filename, printTour = False):
    global TOUR_START_NODE_INDEX

    # read the TSP file provided
    number_of_nodes,costs = readTSPFile(filename)
    #print(costs)

    print("------------------------------------------")
    print("Greedy Algorithm -", filename)
    start_time = time.time()
    i=0
    for i in range(i,number_of_nodes):
        visited.append(0)
    dfs(number_of_nodes,0,costs)
    print("\nPath:", visited_nodes)
    print("Tour length:", "{0:.3f}".format(total_tour_length) )
    print("Total time:", "{0:.3f}".format((time.time() - start_time)), "seconds")
    print("------------------------------------------")


# ---------------------------------------------------------------------------------------------------
# computePathGreedy() method produces the tour using greedy algorithm
# ---------------------------------------------------------------------------------------------------
def dfs(number_of_nodes, i, costs):
    global TOUR_START_NODE_INDEX
    j=0
    global total_tour_length 
    global visited_nodes
    visited[i]=1
    visited_nodes.append(i)
    for j in range(j,number_of_nodes):
        if visited[j]==0:
            if(i==j):
                total_tour_length += 0
            elif(i<j):
                total_tour_length += costs[i,j]
            else:
                total_tour_length += costs[k,i]
            dfs(number_of_nodes,j,costs)
    

# ---------------------------------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    help_description = "The program accepts the path of .TSP file as input and computes the path using Greedy algorithm"
    parser = ArgumentParser(description=help_description)
    parser.add_argument("-file", help="TSP File Path", required=True)
    args = parser.parse_args()
    f_name = args.file

    if os.path.isfile(f_name):
        greedy_main_run(f_name, True)
    else:
        print(f_name,"- File not found. \nPlease make sure the path is correct and try again.")
        exit()
