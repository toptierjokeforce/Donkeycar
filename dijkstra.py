# http://benalexkeen.com/implementing-djikstras-shortest-path-algorithm-with-python/
#repurpose this from Zumi to donkeycar maybe and we can implement shortest path finding given no obstacles

from collections import defaultdict
from zumi.zumi import Zumi
from zumi.protocol import Note
import math
import time

zumi = Zumi()
zumi.mpu.calibrate_MPU(300)
zumi.reset_gyro()


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


graph = Graph()

edges = [
    ('A', 'H', 1), ('A', 'B', 1), ('B', 'C', 1),
    ('C', 'I', 1), ('C', 'D', 1), ('D', 'E', 1),
    ('E', 'J', 1), ('E', 'F', 1), ('F', 'G', 1),
    ('G', 'K', 1), ('H', 'L', 1), ('I', 'N', 1),
    ('J', 'P', 1), ('K', 'R', 1), ('L', 'S', 1),
    ('L', 'M', 1), ('M', 'N', 1), ('N', 'T', 1),
    ('N', 'O', 1), ('O', 'P', 1), ('P', 'U', 1),
    ('P', 'Q', 1), ('Q', 'R', 1), ('R', 'V', 1),
    ('S', 'W', 1), ('T', 'Y', 1), ('U', 'AA', 1),
    ('V', 'AC', 1), ('W', 'AD', 1), ('W', 'X', 1),
    ('X', 'Y', 1), ('Y', 'AE', 1), ('Y', 'Z', 1),
    ('Z', 'AA', 1), ('AA', 'AF', 1), ('AA', 'AB', 1),
    ('AB', 'AC', 1), ('AC', 'AG', 1), ('AD', 'AH', 1),
    ('AE', 'AJ', 1), ('AF', 'AL', 1), ('AG', 'AN', 1),
    ('AH', 'AI', 1), ('AI', 'AJ', 1), ('AJ', 'AK', 1),
    ('AK', 'AL', 1), ('AL', 'AM', 1), ('AM', 'AN', 1),
]

for edge in edges:
    graph.add_edge(*edge)


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


locations = [
    ["AH", 0, 6], ["AI", 1, 6], ["AJ", 2, 6], ["AK", 3, 6], ["AL", 4, 6], ["AM", 5, 6], ["AL", 6, 6],

    ["AD", 0, 5], ["AE", 2, 5], ["AF", 4, 5], ["AG", 6, 5],

    ["W", 0, 4], ["X", 1, 4], ["Y", 2, 4], ["Z", 3, 4], ["AA", 4, 4], ["AB", 5, 4], ["AC", 6, 4],

    ["S", 0, 3], ["T", 2, 3], ["U", 4, 3], ["V", 6, 3],

    ["L", 0, 2], ["M", 1, 2], ["N", 2, 2], ["O", 3, 2], ["P", 4, 2], ["Q", 5, 2], ["R", 6, 2],

    ["H", 0, 1], ["I", 2, 1], ["J", 4, 1], ["K", 6, 1],

    ["A", 0, 0], ["B", 1, 0], ["C", 2, 0], ["D", 3, 0], ["E", 4, 0], ["F", 5, 0], ["G", 6, 0]
]


def giveX(strVal):
    for i in range(len(locations)):
        if strVal == locations[i][0]:
            return locations[i][1]


def giveY(strVal):
    for i in range(len(locations)):
        if strVal == locations[i][0]:
            return locations[i][2]


current_X = 0
current_Y = 0


def node_from_to(start, end):
    global current_X
    global current_Y
    angle = math.atan2((current_Y + giveY(end)) - (current_Y + giveY(start)),
                       (current_X + giveX(end)) - (current_X + giveX(start)))
    zumi.turn(math.degrees(angle), 1.5)
    time = 23 / 14
    zumi.forward(40, time, math.degrees(angle))
    current_X = giveX(end)
    current_Y = giveY(end)


def runner(short):
    for i in range(len(short) - 1):
        node_from_to(short[i], short[i + 1])
