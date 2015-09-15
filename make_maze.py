import random
import sys



n = int(sys.argv[1])
start_x = int(sys.argv[2])
start_y = int(sys.argv[3])
input_seed = int(sys.argv[4])
filename = str(sys.argv[5])

random.seed(input_seed)

visited = {}
#dictionary which initiates the visiting status of all vertices
for x in range(n):
    for y in range(n):
        visited[(x, y)] = False

#dictionary which stores the adjacents of each vertex

#EDGES
adjacency = {(0, 0): [(0, 1), (1, 0)],
                (0, n - 1): [(0, n - 2), (1, n - 1)],
                (n - 1, n - 1): [(n - 1, n - 2), (n - 2 ,n - 1)],
                (n - 1, 0): [(n - 2, 0),(n - 1, 1)]
            }
#PERIMETER
for y in range(1, n - 1):
    adjacency[(0, y)] = [(0, y - 1), (0, y + 1), (1, y)]
    adjacency[(n - 1, y)] = [(n - 1, y - 1), (n - 1, y + 1), (n - 2, y)]
    adjacency[(y, 0)] = [(y + 1, 0), (y - 1, 0),(y, 1)]
    adjacency[(y, n - 1)] = [(y + 1, n - 1), (y - 1, n - 1),(y, n - 2)]

#INNER POINTS
for x in range(1 , n - 1):
    for y in range(1, n - 1):
        adjacency[(x, y)] = [(x - 1, y), (x + 1, y),(x, y - 1), (x, y + 1)]

start = (start_x, start_y)
output = [] #list to hold the output


def form_maze(node):

    visited[node] = True
    random_adjacents = random.sample(adjacency[node], len(adjacency[node]))

    for random_neighbour in random_adjacents:

        if visited[random_neighbour] == False:
            #adds path to the output list
            output.append([node,random_neighbour])
            form_maze(random_neighbour)


    new_file = open(filename, "w+")
    for i in range(len(output) - 1):
        new_file.write(str(output[i][0])+", "+str(output[i][1]))
        new_file.write("\n")
    new_file.close()


form_maze(start)
