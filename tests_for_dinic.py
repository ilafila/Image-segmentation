import math
import time
import sys
from Dinic import Graph

sys.setrecursionlimit(1500)


def test(path):
    print("File test: ", path)
    file = open(path, "r")
    first_line = file.readline().split(' ')
    numberOfNodes = int(first_line[0])
    numberOfEdges = int(first_line[1])
    graph = Graph(n=numberOfNodes, source=1, target=numberOfNodes)
    for i in range(numberOfEdges):
        line = file.readline().split(' ')
        graph.add_edge(int(line[0]), int(line[1]), int(line[2]))
    start = time.time()
    flow = graph.dinic()
    end = time.time()
    print("Time in seconds", "%.3f" % (end - start))
    print('Max flow: ', flow)


# tests 1-6
test("MaxFlow-tests/test_1.txt")
test("MaxFlow-tests/test_2.txt")
test("MaxFlow-tests/test_3.txt")
test("MaxFlow-tests/test_4.txt")
test("MaxFlow-tests/test_5.txt")
test("MaxFlow-tests/test_6.txt")

# tests d1-d5
test("MaxFlow-tests/test_d1.txt")
test("MaxFlow-tests/test_d2.txt")
test("MaxFlow-tests/test_d3.txt")
test("MaxFlow-tests/test_d4.txt")
test("MaxFlow-tests/test_d5.txt")

# tests rd1-rd7
test("MaxFlow-tests/test_rd01.txt")
test("MaxFlow-tests/test_rd02.txt")
test("MaxFlow-tests/test_rd03.txt")
test("MaxFlow-tests/test_rd04.txt")
test("MaxFlow-tests/test_rd05.txt")
test("MaxFlow-tests/test_rd06.txt")
test("MaxFlow-tests/test_rd07.txt")

# tests rl1-rl10
test("MaxFlow-tests/test_rl01.txt")
test("MaxFlow-tests/test_rl02.txt")
test("MaxFlow-tests/test_rl03.txt")
test("MaxFlow-tests/test_rl04.txt")
test("MaxFlow-tests/test_rl05.txt")
test("MaxFlow-tests/test_rl06.txt")
test("MaxFlow-tests/test_rl07.txt")
test("MaxFlow-tests/test_rl08.txt")
test("MaxFlow-tests/test_rl09.txt")
test("MaxFlow-tests/test_rl10.txt")