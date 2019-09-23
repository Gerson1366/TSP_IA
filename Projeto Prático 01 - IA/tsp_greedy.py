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
                    for j in range(i,len(coordenada_x)):
                        #calcula distancia com distancia euclidiana
                        lat1 = coordenada_x[i]
                        lon1 = coordenada_y[i]
                        lat2 = coordenada_x[j]
                        lon2 = coordenada_y[j]
                        dlon = (lon2 - lon1)**2
                        dlat = (lat2 - lat1)**2
                        a = dlat+dlon
                        #c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distance = sqrt(a)
                        #Ignora distancia da cidade para si mesma
                        if(i!=j):
                            costs[i,j] = distance
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

    computePathGreedy(number_of_nodes, TOUR_START_NODE_INDEX, costs, printTour)

    print("Total time:", "{0:.3f}".format((time.time() - start_time)), "seconds")
    print("------------------------------------------")


# ---------------------------------------------------------------------------------------------------
# computePathGreedy() method produces the tour using greedy algorithm
# ---------------------------------------------------------------------------------------------------
def computePathGreedy(number_of_nodes, start_node, costs, printTour):
    global TOUR_START_NODE_INDEX
    visited_nodes = []
    total_tour_length = 0.0
    while (len(visited_nodes) != number_of_nodes-1):
        visited_nodes.append(start_node)
        node_distances = {}
        for key, value in iter(costs.items()):
            if key[0] == start_node and key[0] != key[1] and key[1] not in visited_nodes:
                node_distances[key[1]] = value
            elif key[1] == start_node and key[0] != key[1] and key[0] not in visited_nodes:
                node_distances[key[0]] = value
        start_node = min(node_distances, key=node_distances.get)
        total_tour_length += node_distances.pop(start_node)
    visited_nodes.append(start_node)

    try:
       total_tour_length += costs[start_node, TOUR_START_NODE_INDEX]
    except KeyError:
        total_tour_length += costs[TOUR_START_NODE_INDEX,start_node]

    if printTour:
        print("\nPath:", visited_nodes)
    print("Tour length:", "{0:.3f}".format(total_tour_length) )

# ---------------------------------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    help_description = "The program accepts the path of .TSP file as input and computes the path using Greedy algorithm"
    parser = ArgumentParser(description=help_description)
    parser.add_argument("-file", help="TSP File Path", required=True)
    args = parser.parse_args()
    f_name = args.file
    if(f_name=="brazil58"):
        f_name = 'data/brazil58.tsp'
    elif(f_name=="eil101"):
        f_name = 'data/eil101.tsp'
    elif(f_name=="gil262"):
        f_name = 'data/gil262.tsp'
    else:
        print('Escolha um arquivo valido') 
    if os.path.isfile(f_name):
        greedy_main_run(f_name, True)
    else:
        print(f_name,"- File not found. \nPlease make sure the path is correct and try again.")
        exit()
