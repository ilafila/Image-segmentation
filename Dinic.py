import math
import time


class Edge:
    def __init__(self, a, b, capacity=0, flow=0):
        self.a = a
        self.b = b
        self.cap = capacity
        self.flow = flow


class Graph:
    def __init__(self, n, source, target):
        self.n = n
        self.s = source
        self.t = target
        self.d = []
        self.ptr = [0 for i in range(n+1)]
        self.q = [0 for i in range(n+1)]
        self.e = []
        self.g = [[] for i in range(n+1)]

    def add_edge(self, a, b, capacity):
        e1 = Edge(a, b, capacity)
        e2 = Edge(b, a)
        self.g[a].append(len(self.e))
        self.e.append(e1)
        self.g[b].append(len(self.e))
        self.e.append(e2)

    def bfs(self):
        qh = 1
        qt = 1
        self.q[qt] = self.s
        qt += 1
        self.d = [-1 for i in range(self.n+1)]
        self.d[self.s] = 0
        while qh < qt and self.d[self.t] == -1:
            v = self.q[qh]
            qh += 1
            for i in range(len(self.g[v])):
                id = self.g[v][i]
                to = self.e[id].b
                if self.d[to] == -1 and self.e[id].flow < self.e[id].cap:
                    self.q[qt] = to
                    qt += 1
                    self.d[to] = self.d[v] + 1
        return self.d[self.t] != -1

    def dfs(self, v, flow):
        if not flow:
            return 0
        if v == self.t:
            return flow
        while self.ptr[v] < len(self.g[v]):
            id = self.g[v][self.ptr[v]]
            to = self.e[id].b
            if self.d[to] != self.d[v] + 1:
                self.ptr[v] += 1
                continue
            pushed = self.dfs(to, min(flow, self.e[id].cap - self.e[id].flow))
            if pushed:
                self.e[id].flow += pushed
                self.e[id ^ 1].flow -= pushed
                return pushed
            self.ptr[v] += 1
        return 0

    def dinic(self):
        flow = 0
        while True:
            if not self.bfs():
                break
            self.ptr = [0 for i in range(self.n+1)]
            pushed = self.dfs(self.s, math.inf)
            while pushed:
                flow += pushed
                pushed = self.dfs(self.s, math.inf)
        return flow


def test(path):
    print("file test: ", path)
    file = open(path, "r")
    first_line = file.readline().split(' ')
    numberOfNodes = int(first_line[0])  # количество вершин
    numberOfEdges = int(first_line[1])
    graph = Graph(n=numberOfNodes, source=1, target=numberOfNodes)
    for i in range(numberOfEdges):
        line = file.readline().split(' ')
        print(int(line[0]))
        print(int(line[1]))
        print(int(line[2]))
        graph.add_edge(int(line[0]), int(line[1]), int(line[2]))
    flow = graph.dinic()
    print('Flow: ', flow)


# tests 1-6
# test("MaxFlow-tests/test_1.txt")
# test("MaxFlow-tests/test_2.txt")
# test("MaxFlow-tests/test_3.txt")
# test("MaxFlow-tests/test_4.txt")
# test("MaxFlow-tests/test_5.txt")
# test("MaxFlow-tests/test_6.txt")
#
# # tests d1-d5
# test("MaxFlow-tests/test_d1.txt")
# test("MaxFlow-tests/test_d2.txt")
# test("MaxFlow-tests/test_d3.txt")
test("MaxFlow-tests/test_d4.txt")
# test("MaxFlow-tests/test_d5.txt")
#
# # tests rd1-rd7
# test("MaxFlow-tests/test_rd01.txt")
# test("MaxFlow-tests/test_rd02.txt")
# test("MaxFlow-tests/test_rd03.txt")
# test("MaxFlow-tests/test_rd04.txt")
# test("MaxFlow-tests/test_rd05.txt")
# test("MaxFlow-tests/test_rd06.txt")
# test("MaxFlow-tests/test_rd07.txt")
#
# # tests rl1-rl10
# test("MaxFlow-tests/test_rl01.txt")
# test("MaxFlow-tests/test_rl02.txt")
# test("MaxFlow-tests/test_rl03.txt")
# test("MaxFlow-tests/test_rl04.txt")
# test("MaxFlow-tests/test_rl05.txt")
# test("MaxFlow-tests/test_rl06.txt")
# test("MaxFlow-tests/test_rl07.txt")
# test("MaxFlow-tests/test_rl08.txt")
# test("MaxFlow-tests/test_rl09.txt")
# test("MaxFlow-tests/test_rl10.txt")