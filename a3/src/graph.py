import random
from collections import defaultdict
from typing import Union, Tuple


class TRIESTGraph:
    def __init__(self):
        self._S = []
        self._neighbors = defaultdict(set)

    def get_size(self) -> int:
        return len(self._S)

    def in_graph(self, u: int, v: int) -> bool:
        if u < v:
            return (u, v) in self._S
        else:
            return (v, u) in self._S

    def add_edge(self, u: int, v: int) -> None:
        # keep the order of elements in tuples
        if u < v:
            self._S.append((u, v))
        else:
            self._S.append((v, u))
        self.modify_neighbors(u, v, '+')

    def remove_edge(self, u: int, v: int) -> None:
        if u < v:
            self._S.remove((u, v))
        else:
            self._S.remove((v, u))
        self.modify_neighbors(u, v, '-')

    def random_select_edge(self) -> Tuple[int, int]:
        random_choice = random.randint(0, len(self._S) - 1)
        u_chosen, v_chosen = self._S[random_choice]
        return (u_chosen, v_chosen) if u_chosen < v_chosen else (v_chosen, u_chosen)

    def modify_neighbors(self, u: int, v: int, op: str) -> None:
        if op == '+':
            self._neighbors[u].add(v)
            self._neighbors[v].add(u)

        elif op == '-':
            if self._neighbors[u]: self._neighbors[u].discard(v)

            if self._neighbors[v]: self._neighbors[v].discard(u)

            if not self._neighbors[u]: del self._neighbors[u]

            if not self._neighbors[v]: del self._neighbors[v]

    def get_intersection_neighbors(self, u: int, v: int) -> Union[set, None]:
        if u in self._neighbors and v in self._neighbors:
            return self._neighbors[u].intersection(self._neighbors[v])
        else:
            return None
