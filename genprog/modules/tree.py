from copy import deepcopy
from typing import List
from random import choice
from genprog.modules.node import Node

grow = 0
full = 1

class Chormossome:
    def __init__(self, max_depth: int, terminals: List[Node], non_terminals: List[Node]):
        self.terminals: List[Node] = terminals
        self.non_terminals: List[Node] = non_terminals
        self.all: List[Node] = non_terminals + terminals
        self.max_depth: int = max_depth
        self.depth = 0
        self.count = 0

    def build(self, depth, methods: List[int]) -> Node:
        if depth > self.depth:
            self.depth = depth

        self.count += 1


        if depth == self.max_depth:
            node = deepcopy(choice(self.terminals))
            node.idx = self.count
            print(depth, '|', node.idx, '|', node.handle)        

            return node
        
        method = choice(methods)

        if method == grow:
            node = deepcopy(choice(self.all))
        else:
            node = deepcopy(choice(self.non_terminals))

        node.idx = self.count
        print(depth, '|', node.idx, '|', node.handle)        

        if node.is_terminal():
            return node
        
        for _ in range(2):
            node.children.append(self.build(depth + 1, methods))
        return node

