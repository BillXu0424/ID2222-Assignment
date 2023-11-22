from graph import TRIESTGraph
from collections import defaultdict
import random


class TriestBase:
    def __init__(self, M: int, filename: str) -> None:
        self._M = M
        self._filename = filename
        self._subgraph = TRIESTGraph()
        self._t = 0
        self._tau = 0  # global estimation
        self._taus = defaultdict(int)  # local estimation

    def process(self):
        f = open(self._filename, "r")
        line = f.readline()
        while line:
            u, v = map(lambda a: int(a), line.split())
            self._t += 1
            if self.sample_edge(u, v):
                self._subgraph.add_edge(u, v)
                self.update_counters(u, v, '+')
            line = f.readline()
        f.close()
        return self._tau * max(1, int((self._t * (self._t - 1) * (self._t - 2))/(self._M * (self._M - 1) * (self._M - 2))))

    def sample_edge(self, u: int, v: int) -> bool:
        if self._t <= self._M:
            return True
        elif random.random() < self._M / self._t:
            u_prime, v_prime = self._subgraph.random_select_edge()
            self._subgraph.remove_edge(u_prime, v_prime)
            self.update_counters(u_prime, v_prime, '-')
            return True
        return False

    def update_counters(self, u: int, v: int, op: str) -> None:
        common_neighbors = self._subgraph.get_intersection_neighbors(u, v)
        if common_neighbors is None:
            return
        for c in common_neighbors:
            if op == '+':
                self._tau += 1
                self._taus[c] += 1
                self._taus[u] += 1
                self._taus[v] += 1
            else:
                self._tau = self._tau - 1 if self._tau > 0 else 0
                self._taus[c] -= 1
                self._taus[u] -= 1
                self._taus[v] -= 1


class TriestImpr:
    def __init__(self, M: int, filename: str) -> None:
        self._M = M
        self._filename = filename
        self._subgraph = TRIESTGraph()
        self._t = 0
        self._tau = 0  # global estimation
        self._taus = defaultdict(int)  # local estimation

    def process(self):
        f = open(self._filename, "r")
        line = f.readline()
        while line:
            u, v = map(lambda a: int(a), line.split())
            self._t += 1
            self.update_counters(u, v)
            if self.sample_edge(u, v):
                self._subgraph.add_edge(u, v)
            line = f.readline()
        f.close()
        return self._tau

    def sample_edge(self, u: int, v: int) -> bool:
        if self._t <= self._M:
            return True
        elif random.random() < self._M / self._t:
            u_prime, v_prime = self._subgraph.random_select_edge()
            self._subgraph.remove_edge(u_prime, v_prime)
            return True
        return False

    def update_counters(self, u: int, v: int) -> None:
        common_neighbors = self._subgraph.get_intersection_neighbors(u, v)
        if common_neighbors is None:
            return
        eta_t = max(1, int(((self._t-1)*(self._t-2))/(self._M * (self._M - 1))))
        for c in common_neighbors:
            self._tau += eta_t
            self._taus[c] += eta_t
            self._taus[u] += eta_t
            self._taus[v] += eta_t
