# Written by Gavin Mack
# September 2016
from collections import deque

graph = {
'arad': ['sibiu', 'timisoara', 'zerind'],
'bucharest': ['fagaras', 'giurgiu', 'pitesti', 'urziceni'],
'craiova': ['dobreta', 'pitesti', 'rimnicu_vilcea'],
'dobreta': ['craiova', 'mehadia'],
'eforie': ['hirsova'],
'fagaras': ['bucharest', 'sibiu'],
'giurgiu': ['bucharest'],
'hirsova': ['eforie', 'urziceni'],
'iasi': ['neamt', 'vaslui'],
'lugoj': ['mehadia', 'timisoara'],
'mehadia': ['dobreta', 'lugoj'],
'neamt': ['iasi'],
'oradea': ['sibiu', 'zerind'],
'pitesti': ['bucharest', 'craiova', 'rimnicu_vilcea'],
'rimnicu_vilcea': ['craiova', 'pitesti', 'sibiu'],
'sibiu': ['arad', 'fagaras', 'oradea', 'rimnicu_vilcea'],
'timisoara': ['arad', 'lugoj'],
'urziceni': ['bucharest', 'hirsova', 'vaslui'],
'vaslui': ['iasi', 'urziceni'],
'zerind': ['arad', 'oradea']
}


def BFS(start, goal):
	paths = deque([])
	paths.append([start])
	expanded = [start]
	while paths:
		path = paths.popleft()#curr is list of paths
		if path[-1] == goal:#if last element on path list is goal city
			return path, expanded
		else:
			#generate multiple additional paths consisting of current path + each successor
			#push each new path on back of queue
			for successor in graph[path[-1]]:
				#generate new paths
				if successor not in expanded:#if the node has not been explored
					expanded.append(successor)#add the new node to the list of expanded nodes
					newpath = list(path)#make copy of current path
					newpath.append(successor)#append each successor onto the newpath
					paths.append(newpath)#append the newpath onto the paths list
	return [], expanded


def DFS(start, goal):
	paths = []
	paths.append([start])
	expanded = [start]
	while paths:
		path = paths.pop()#curr is list of paths
		if path[-1] == goal:#if last element on path list is goal city
			return path, expanded
		else:
			#generate multiple additional paths consisting of current path + each successor
			#push each new path on top of stack
			for successor in graph[path[-1]]:
				#generate new paths
				if successor not in expanded:#if the node has not been explored
					expanded.append(successor)#add the new node to the list of expanded nodes
					newpath = list(path)#make copy of current path
					newpath.append(successor)#append each successor onto the newpath
					paths.append(newpath)#append the newpath onto the paths list
	return [], expanded


BFS_path1, BFS_expanded1 = BFS('lugoj', 'bucharest')
BFS_path2, BFS_expanded2 = BFS('bucharest', 'lugoj')
DFS_path1, DFS_expanded1 = DFS('lugoj', 'bucharest')
DFS_path2, DFS_expanded2 = DFS('bucharest', 'lugoj')

print "DFS path lugoj to bucharest:"
for city in DFS_path1:
	print city
"""
print "DFS nodes expanded lugoj to bucharest:"
for expanded_node in DFS_expanded1:
	print expanded_node
"""
print "Number of nodes expanded: ", len(DFS_expanded1)
print ""
print "DFS path bucharest to lugoj:"
for city in DFS_path2:
	print city
print "Number of nodes expanded: ", len(DFS_expanded2)
print ""
print "BFS path lugoj to bucharest:"
for city in BFS_path1:
	print city
print "Number of nodes expanded: ", len(BFS_expanded1)
print ""
print "BFS path bucharest to lugoj:"
for city in BFS_path2:
	print city
print "Number of nodes expanded: ", len(BFS_expanded2)
