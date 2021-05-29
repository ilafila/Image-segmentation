import math
import time
import sys

sys.setrecursionlimit(1500)


class Edge:
    def __init__(self, a, b, capacity=0, flow=0):
        self.a = a
        self.b = b
        self.cap = capacity
        self.flow = flow

    def add_capacity(self, plus_cap):
        self.cap += plus_cap


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

        self.reachable = set()

    def add_edge(self, a, b, capacity):
        e1 = Edge(a, b, capacity)
        e2 = Edge(b, a)
        self.g[a].append(len(self.e))
        self.e.append(e1)
        self.g[b].append(len(self.e))
        self.e.append(e2)

    def add_to_edge(self, v, to, cap):
        for i in range(len(self.g[v])):
            id = self.g[v][i]
            if to == self.e[id].b:
                self.e[id].add_capacity(cap)
        return 0

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

    def simple_dfs(self, v):
        self.reachable[v] = 1
        ptr = 0
        while ptr < len(self.g[v]):
            edge_id = self.g[v][ptr]
            to = self.e[edge_id].b
            flow = self.e[edge_id].flow
            cap = self.e[edge_id].cap
            if 0 < flow < cap and not self.reachable[to]:
                self.simple_dfs(to)
            ptr += 1
        return 0

    def min_cut(self):
        self.reachable = [0 for i in range(self.n)]
        self.simple_dfs(self.s)
        return self.reachable[:-2]
