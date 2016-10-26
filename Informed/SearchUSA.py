# Written by Gavin Mack
# To be run with python SearchUSA.py search start goal
# Last modified October 2016
from node import Node
from Queue import PriorityQueue
from MyPQ import MyPriorityQueue
import math
import sys, getopt

# reference last element of list with list[-1]

# NOTE: represent neighbors as graph instead of list: keys = neighbor cities, values = path_cost from outer key
# graph containing key = city, value = list of lists, first list contains [lat, long], second list contains neighboring cities
USA_graph = {
    'albanyGA': [[31.58, 84.17], {'macon': 106, 'tallahassee': 120}],
    'albanyNY': [[42.66, 73.78], {'boston': 166, 'montreal': 226, 'rochester': 148}],
    'albuquerque': [[35.11, 106.61], {'elPaso': 267, 'santaFe': 61}],
    'atlanta': [[33.76, 84.40], {'chattanooga': 117, 'macon': 82}],
    'augusta': [[33.43, 82.02], {'charlotte': 161, 'savannah': 131}],
    'austin': [[30.30, 97.75], {'houston': 186, 'sanAntonio': 79}],
    'bakersfield': [[35.36, 119.03], {'fresno': 107, 'losAngeles': 112}],
    'baltimore': [[39.31, 76.62], {'philadelphia': 102, 'washington': 45}],
    'batonRouge': [[30.46, 91.14], {'lafayette': 50, 'newOrleans': 80}],
    'beaumont': [[30.08, 94.13], {'houston': 69, 'lafayette': 122}],
    'boise': [[43.61, 116.24], {'portland': 428, 'saltLakeCity': 349}],
    'boston': [[42.32, 71.09], {'albanyNY': 166, 'providence': 51}],
    'buffalo': [[42.90, 78.85], {'cleveland': 191, 'rochester': 64, 'toronto': 105}],
    'calgary': [[51.00, 114.00], {'vancouver': 605, 'winnipeg': 829}],
    'charlotte': [[35.21, 80.83], {'augusta': 161, 'greensboro': 91}],
    'chattanooga': [[35.05, 85.27], {'atlanta': 117, 'nashville': 129}],
    'chicago': [[41.84, 87.68], {'midland': 279, 'milwaukee': 90}],
    'cincinnati': [[39.14, 84.50], {'dayton': 56, 'indianapolis': 110}],
    'cleveland': [[41.48, 81.67], {'buffalo': 191, 'columbus': 142, 'pittsburgh': 157}],
    'coloradoSprings': [[38.86, 104.79], {'denver': 70, 'santaFe': 316}],
    'columbus': [[39.99, 82.99], {'cleveland': 142, 'dayton': 72}],
    'dallas': [[32.80, 96.79], {'denver': 792, 'mexia': 83}],
    'dayton': [[39.76, 84.20], {'cincinnati': 56, 'columbus': 72}],
    'daytonaBeach': [[29.21, 81.04], {'jacksonville': 92, 'orlando': 54}],
    'denver': [[39.73, 104.97], {'coloradoSprings': 70, 'dallas': 792, 'grandJunction': 246, 'wichita': 523}],
    'desMoines': [[41.59, 93.62], {'minneapolis': 246, 'omaha': 135}],
    'elPaso': [[31.79, 106.42], {'albuquerque': 267, 'sanAntonio': 580, 'tucson': 320}],
    'eugene': [[44.06, 123.11], {'medford': 165, 'salem': 63}],
    'europe': [[48.87, -2.33], {'philadelphia': 3939}],
    'ftWorth': [[32.74, 97.33], {'oklahomaCity': 209}],
    'fresno': [[36.78, 119.79], {'bakersfield': 107, 'modesto': 109}],
    'grandJunction': [[39.08, 108.56], {'denver': 246, 'provo': 220}],
    'greenBay': [[44.51, 88.02], {'milwaukee': 117, 'minneapolis': 304}],
    'greensboro': [[36.08, 79.82], {'charlotte': 91, 'raleigh': 74}],
    'houston': [[29.76, 95.38], {'austin': 186, 'beaumont': 69, 'mexia': 165}],
    'indianapolis': [[39.79, 86.15], {'cincinnati': 110, 'stLouis': 246}],
    'jacksonville': [[30.32, 81.66], {'daytonaBeach': 92, 'lakeCity': 113, 'savannah': 140}],
    'japan': [[35.68, 220.23], {'pointReyes': 5131, 'sanLuisObispo': 5451}],
    'kansasCity': [[39.08, 94.56], {'stLouis': 256, 'tulsa': 249, 'wichita': 190}],
    'keyWest': [[24.56, 81.78], {'tampa': 446}],
    'lafayette': [[30.21, 92.03], {'batonRouge': 50, 'beaumont': 122}],
    'lakeCity': [[30.19, 82.64], {'jacksonville': 113, 'tallahassee': 104, 'tampa': 169}],
    'laredo': [[27.52, 99.49], {'mexico': 741, 'sanAntonio': 154}],
    'lasVegas': [[36.19, 115.22], {'losAngeles': 275, 'saltLakeCity': 486}],
    'lincoln': [[40.81, 96.68], {'omaha': 58, 'wichita': 277}],
    'littleRock': [[34.74, 92.33], {'memphis': 137, 'tulsa': 276}],
    'losAngeles': [[34.03, 118.17], {'bakersfield': 112, 'lasVegas': 275, 'sanDiego': 124, 'sanLuisObispo': 182}],
    'macon': [[32.83, 83.65], {'albanyGA': 106, 'atlanta': 82}],
    'medford': [[42.33, 122.86], {'eugene': 165, 'redding': 150}],
    'memphis': [[35.12, 89.97], {'littleRock': 137, 'nashville': 210}],
    'mexia': [[31.68, 96.48], {'dallas': 83, 'houston': 165}],
    'mexico': [[19.40, 99.12], {'laredo': 741}],
    'miami': [[25.79, 80.22], {'westPalmBeach': 67}],
    'midland': [[43.62, 84.23], {'chicago': 279, 'toledo': 82}],
    'milwaukee': [[43.05, 87.96], {'chicago': 90, 'greenBay': 117}],
    'minneapolis': [[44.96, 93.27], {'desMoines': 246, 'greenBay': 304, 'winnipeg': 463}],
    'modesto': [[37.66, 120.99], {'fresno': 109, 'stockton': 29}],
    'montreal': [[45.50, 73.67], {'albanyNY': 226, 'ottawa': 132}],
    'nashville': [[36.15, 86.76], {'chattanooga': 129, 'memphis': 210}],
    'newHaven': [[41.31, 72.92], {'providence': 110, 'stamford': 92}],
    'newOrleans': [[29.97, 90.06], {'batonRouge': 80, 'pensacola': 268}],
    'newYork': [[40.70, 73.92], {'philadelphia': 101}],
    'norfolk': [[36.89, 76.26], {'raleigh': 174, 'richmond': 92}],
    'oakland': [[37.80, 122.23], {'sanFrancisco': 8, 'sanJose': 42}],
    'oklahomaCity': [[35.48, 97.53], {'ftWorth': 209, 'tulsa': 105}],
    'omaha': [[41.26, 96.01], {'desMoines': 135, 'lincoln': 58}],
    'orlando': [[28.53, 81.38], {'daytonaBeach': 54, 'tampa': 84, 'westPalmBeach': 168}],
    'ottawa': [[45.42, 75.69], {'montreal': 132, 'toronto': 269}],
    'pensacola': [[30.44, 87.21], {'newOrleans': 268, 'tallahassee': 120}],
    'philadelphia': [[40.72, 76.12], {'baltimore': 102, 'europe': 3939, 'newYork': 101, 'pittsburgh': 319, 'uk1': 3548, 'uk2': 3548}],
    'phoenix': [[33.53, 112.08], {'tucson': 117, 'yuma': 178}],
    'pittsburgh': [[40.40, 79.84], {'cleveland': 157, 'philadelphia': 319}],
    'pointReyes': [[38.07, 122.81], {'japan': 5131, 'redding': 215, 'sacramento': 115}],
    'portland': [[45.52, 122.64], {'boise': 428, 'salem': 47, 'seattle': 174}],
    'providence': [[41.80, 71.36], {'boston': 51, 'newHaven': 110}],
    'provo': [[40.24, 111.66], {'grandJunction': 220}],
    'raleigh': [[35.82, 78.64], {'greensboro': 74, 'norfolk': 174}],
    'redding': [[40.58, 122.37], {'medford': 150, 'pointReyes': 215}],
    'reno': [[39.53, 119.82], {'sacramento': 133, 'saltLakeCity': 520}],
    'richmond': [[37.54, 77.46], {'norfolk': 92, 'washington': 105}],
    'rochester': [[43.17, 77.61], {'albanyNY': 148, 'buffalo': 64}],#DONE
    'sacramento': [[38.56, 121.47], {'pointReyes': 115, 'reno': 133, 'sanFrancisco': 95, 'stockton': 51}],
    'salem': [[44.93, 123.03], {'eugene': 63, 'portland': 47}],
    'salinas': [[36.68, 121.64], {'sanJose': 31, 'sanLuisObispo': 137}],
    'saltLakeCity': [[40.75, 111.89], {'boise': 349, 'lasVegas': 486, 'reno': 520}],
    'sanAntonio': [[29.45, 98.51], {'austin': 79, 'elPaso': 580, 'laredo': 154}],
    'sanDiego': [[32.78, 117.15], {'losAngeles': 124, 'yuma': 172}],
    'sanFrancisco': [[37.76, 122.44], {'oakland': 8, 'sacramento': 95}],
    'sanJose': [[37.30, 121.87], {'oakland': 42, 'salinas': 31}],
    'sanLuisObispo': [[35.27, 120.66], {'japan': 5451, 'losAngeles': 182, 'salinas': 137}],
    'santaFe': [[35.67, 105.96], {'albuquerque': 61, 'coloradoSprings': 316}],
    'saultSteMarie': [[46.49, 84.35], {'thunderBay': 442, 'toronto': 436}],
    'savannah': [[32.05, 81.10], {'augusta': 131, 'jacksonville': 140}],
    'seattle': [[47.63, 122.33], {'portland': 174, 'vancouver': 115}],
    'stLouis': [[38.63, 90.24], {'indianapolis': 246, 'kansasCity': 256}],
    'stamford': [[41.07, 73.54], {'newHaven': 92}],
    'stockton': [[37.98, 121.30], {'modesto': 29, 'sacramento': 51}],
    'tallahassee': [[30.45, 84.27], {'albanyGA': 120, 'lakeCity': 104, 'pensacola': 120}],
    'tampa': [[27.97, 82.46], {'keyWest': 446, 'lakeCity': 169, 'orlando': 84}],
    'thunderBay': [[48.38, 89.25], {'saultSteMarie': 442, 'winnipeg': 440}],
    'toledo': [[41.67, 83.58], {'midland': 82}],
    'toronto': [[43.65, 79.38], {'buffalo': 105, 'ottawa': 269, 'saultSteMarie': 436}],
    'tucson': [[32.21, 110.92], {'elPaso': 320, 'phoenix': 117}],
    'tulsa': [[36.13, 95.94], {'kansasCity': 249, 'littleRock': 276, 'oklahomaCity': 105}],
    'uk1': [[51.30, 0.00], {'philadelphia': 3548}],
    'uk2': [[51.30, 0.00], {'philadelphia': 3548}],
    'vancouver': [[49.25, 123.10], {'calgary': 605, 'seattle': 115}],
    'washington': [[38.91, 77.01], {'baltimore': 45, 'richmond': 105}],
    'westPalmBeach': [[26.71, 80.05], {'miami': 67, 'orlando': 168}],
    'wichita': [[37.69, 97.34], {'denver': 523, 'kansasCity': 190, 'lincoln': 277}],
    'winnipeg': [[49.90, 97.13], {'calgary': 829, 'minneapolis': 463, 'thunderBay': 440}],
    'yuma': [[32.69, 114.62], {'phoenix': 178, 'sanDiego': 172}]
}

#Keep track of nodes expanded and compute the number of expanded nodes
#access graph neighbors with USA_graph['city_name'][1], returns list of neighbors
"""
print(USA_graph['yuma'][0][0])

print(USA_graph['yuma'][0][1])
"""

def heuristic(city1, city2):
    lat1 = USA_graph[city1][0][0]
    lon1 = USA_graph[city1][0][1]
    lat2 = USA_graph[city2][0][0]
    lon2 = USA_graph[city2][0][1]
    return math.sqrt((69.5*(lat1-lat2))**2 + (69.5*math.cos((lat1+lat2)/360*math.pi) * (lon1-lon2))**2)


def cost_from(city1, city2):
    #Returns the cost of the edge from city1 to city2
    return USA_graph[city1][1][city2]


# Start and goal are both strings of the cities
def astar(start, goal):
    #Need to declare node which contains path list and cost_so_far
    start_node = Node(0, [start])
    frontier = PriorityQueue()
    start_priority = start_node.cost_so_far + heuristic(start, goal)
    frontier.put(start_node, start_priority)      #place start node on queue
    frontier_list = {start: start_node.cost_so_far} #unordered dict key= cities in PQ with val= cost_so_far
    expanded = []
    first = True

    while not frontier.empty():
        if first:
            node = frontier.get()
        else:
            node = frontier.get()[1]
        first = False
        #print('path = ', node.path)
        city_to_remove = node.path[-1]
        #print('frontier_list = ', frontier_list)
        #print('city_to_remove = ', city_to_remove)
        #frontier_list.pop(city_to_remove) #removes curr city name from frontier_list
        del frontier_list[city_to_remove]
        #print(node.path)
        # add currnode to expanded TODO: verify this is correct
        if node.path[-1] not in expanded:
            expanded.append(node.path[-1])

        if node.path[-1] == goal: #if we're at our goal
            return node, expanded

        #loop through neighbors of node:
        #if neighbors is a graph, loop through with: for neighbor in USA_graph['city_name'][1]:
        #print(USA_graph[node.path[-1]][1])
        for neighbor in USA_graph[node.path[-1]][1]:
            #neighbor is each neighbor as a string

            # try making tmp copy of frontier and iterate through removing nodes to check if neighbor in frontier
            if neighbor not in expanded and neighbor not in frontier_list:
                # need to add city to frontier_list whenever I add node to frontier
                # calculate priority
                # create node, add node with correct priority to frontier
                # add correct city to frontier_list
                new_cost_so_far = node.cost_so_far + cost_from(node.path[-1], neighbor)
                # create new path and populate with node.path + neighbor
                new_path = []
                for city in node.path:
                    new_path.append(city)
                new_path.append(neighbor)
                #print(node.path)
                new_node = Node(new_cost_so_far, new_path)
                #print(node.path)
                frontier_list[neighbor] = new_cost_so_far
                prior = new_cost_so_far + heuristic(neighbor, goal)
                frontier.put((prior, new_node)) # add node with priority

            elif neighbor in frontier_list: #and (frontier_list[neighbor] + cost_from(neighbor, goal) < prior curr in frontier
                frontier_prior = frontier_list[neighbor] + heuristic(neighbor, goal)
                new_path_prior = node.cost_so_far + cost_from(node.path[-1], neighbor) + heuristic(neighbor, goal)
                if frontier_prior > new_path_prior:
                    # replace frontier node with new child node
                    # NOTE: Incredibly inefficient, just need way to remove specific node from PQ but this works
                    tmp_frontier = PriorityQueue()
                    while not frontier.empty():
                        tmp_node = frontier.get()[1]
                        if neighbor == tmp_node.path[-1]:
                            # Found important node, modify frontier and frontier_list appropriately
                            #new_path = node.path
                            #tmp_node.path = new_path.append(neighbor)
                            new_path = []
                            for city in node.path:
                                new_path.append(city)
                            new_path.append(neighbor)
                            tmp_node.path = new_path
                            # update cost_so_far of tmp_node
                            new_cost_so_far = node.cost_so_far + cost_from(node.path[-1], neighbor)
                            # update frontier_list
                            frontier_list[neighbor] = new_cost_so_far
                            # add tmp_node back into frontier
                            prior = new_cost_so_far + heuristic(neighbor, goal)
                            tmp_frontier.put((prior, tmp_node))
                        else:
                            #reinsert with correct priority
                            prior = tmp_node.cost_so_far + heuristic(tmp_node.path[-1], goal)
                            tmp_frontier.put((prior, tmp_node))
                    while not tmp_frontier.empty():
                        # Replace everything into frontier
                        tmp_node = tmp_frontier.get()[1]
                        prior = tmp_node.cost_so_far + heuristic(tmp_node.path[-1], goal)
                        frontier.put((prior, tmp_node))

    return Node(0, []), expanded


# Start and goal are both strings of the cities
def uniform(start, goal):
    #Need to declare node which contains path list and cost_so_far
    start_node = Node(0, [start])
    frontier = MyPriorityQueue()
    start_priority = start_node.cost_so_far
    frontier.add_task(start_node, start_priority)      #place start node on queue
    frontier_list = {start: start_node.cost_so_far} #unordered dict key= cities in PQ with val= cost_so_far
    expanded = []
    first = True

    while not frontier.empty():
        node = frontier.pop_task()
        city_to_remove = node.path[-1]
        del frontier_list[city_to_remove]
        # add currnode to expanded
        if node.path[-1] not in expanded:
            expanded.append(node.path[-1])

        if node.path[-1] == goal: #if we're at our goal
            return node, expanded

        #loop through neighbors of node:
        #if neighbors is a graph, loop through with: for neighbor in USA_graph['city_name'][1]:
        #print(USA_graph[node.path[-1]][1])
        for neighbor in USA_graph[node.path[-1]][1]:
            #neighbor is each neighbor as a string

            # try making tmp copy of frontier and iterate through removing nodes to check if neighbor in frontier
            if neighbor not in expanded and neighbor not in frontier_list:
                # need to add city to frontier_list whenever I add node to frontier
                # calculate priority
                # create node, add node with correct priority to frontier
                # add correct city to frontier_list
                new_cost_so_far = node.cost_so_far + cost_from(node.path[-1], neighbor)
                # create new path and populate with node.path + neighbor
                new_path = []
                for city in node.path:
                    new_path.append(city)
                new_path.append(neighbor)
                #print(node.path)
                new_node = Node(new_cost_so_far, new_path)
                #print(node.path)
                frontier_list[neighbor] = new_cost_so_far
                prior = new_cost_so_far
                frontier.add_task(new_node, prior) # add node with priority

            elif neighbor in frontier_list: #and (frontier_list[neighbor] + cost_from(neighbor, goal) < prior curr in frontier
                frontier_prior = frontier_list[neighbor]
                new_path_prior = node.cost_so_far + cost_from(node.path[-1], neighbor)
                if frontier_prior > new_path_prior:
                    # replace frontier node with new child node
                    # NOTE: Incredibly inefficient, just need way to remove specific node from PQ but this works
                    tmp_frontier = MyPriorityQueue()
                    while not frontier.empty():
                        tmp_node = frontier.pop_task()
                        if neighbor == tmp_node.path[-1]:
                            # Found important node, modify frontier and frontier_list appropriately
                            #new_path = node.path
                            #tmp_node.path = new_path.append(neighbor)
                            new_path = []
                            for city in node.path:
                                new_path.append(city)
                            new_path.append(neighbor)
                            tmp_node.path = new_path
                            # update cost_so_far of tmp_node
                            new_cost_so_far = node.cost_so_far + cost_from(node.path[-1], neighbor)
                            # update frontier_list
                            frontier_list[neighbor] = new_cost_so_far
                            # add tmp_node back into frontier
                            prior = new_cost_so_far
                            tmp_frontier.add_task(tmp_node, prior)
                        else:
                            #reinsert with correct priority
                            prior = tmp_node.cost_so_far
                            tmp_frontier.add_task(tmp_node, prior)
                    while not tmp_frontier.empty():
                        # Replace everything into frontier
                        tmp_node = tmp_frontier.pop_task()
                        prior = tmp_node.cost_so_far
                        frontier.add_task(tmp_node, prior)

    return Node(0, []), expanded


# Greedy should be similar to A*, except no elif and priority = h(n) instead of h(n) + cost_so_far
# Start and goal are both strings of the cities
def greedy(start, goal):
    # Need to declare node which contains path list and cost_so_far
    start_node = Node(0, [start])
    frontier = PriorityQueue()
    start_priority = heuristic(start, goal)
    frontier.put(start_node, start_priority)      #place start node on queue
    frontier_list = {start: start_node.cost_so_far} #unordered dict key= cities in PQ with val= cost_so_far
    expanded = []
    first = True

    while not frontier.empty():
        if first:
            node = frontier.get()
        else:
            node = frontier.get()[1]
        first = False
        #print('path = ', node.path)
        city_to_remove = node.path[-1]
        del frontier_list[city_to_remove]
        # add currnode to expanded
        if node.path[-1] not in expanded:
            expanded.append(node.path[-1])

        if node.path[-1] == goal:  # if we're at our goal
            return node, expanded

        # loop through neighbors of node:
        # if neighbors is a graph, loop through with: for neighbor in USA_graph['city_name'][1]:
        # print(USA_graph[node.path[-1]][1])
        for neighbor in USA_graph[node.path[-1]][1]:
            # neighbor is each neighbor as a string

            # try making tmp copy of frontier and iterate through removing nodes to check if neighbor in frontier
            if neighbor not in expanded and neighbor not in frontier_list:
                # need to add city to frontier_list whenever I add node to frontier
                # calculate priority
                # create node, add node with correct priority to frontier
                # add correct city to frontier_list
                new_cost_so_far = node.cost_so_far + cost_from(node.path[-1], neighbor)
                # create new path and populate with node.path + neighbor
                new_path = []
                for city in node.path:
                    new_path.append(city)
                new_path.append(neighbor)
                new_node = Node(new_cost_so_far, new_path)
                frontier_list[neighbor] = new_cost_so_far
                prior = heuristic(neighbor, goal)
                frontier.put((prior, new_node)) # add node with priority

    return Node(0, []), expanded


if __name__ == "__main__":
    search = sys.argv[1]
    start_city = sys.argv[2]
    goal_city = sys.argv[3]

    if search == 'astar':
        result_node, expanded_list = astar(start_city, goal_city)
    elif search == 'uniform':
        result_node, expanded_list = uniform(start_city, goal_city)
    elif search == 'greedy':
        result_node, expanded_list = greedy(start_city, goal_city)
    else:
        print("Invalid input, arguments should be 'search start goal'")
        sys.exit(2)

    print'Path: ', result_node.path
    print'Path length: ', len(result_node.path)
    print'Distance traveled: ', result_node.cost_so_far
    print'Expanded list length:', len(expanded_list)
    print'Expanded list: ', expanded_list
