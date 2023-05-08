from copy import deepcopy
from typing import List
from random import choice, randint
from genprog.modules.node import Node, bfs_find_parent

grow = 0
full = 1

class Chormossome:
    def __init__(self, max_depth: int, methods: List[int], terminals: List[Node], non_terminals: List[Node]):
        self.terminals: List[Node] = terminals
        self.non_terminals: List[Node] = non_terminals
        self.max_depth: int = max_depth
        self.root, self.depth = build(0,max_depth,methods, terminals, non_terminals)

    def crossover_choice(self) -> tuple[Node, int]:
        co_depth = randint(1, self.depth)
        bits = [0,1]
        moves = []
        for _ in range(co_depth):
            moves.append(choice(bits))

        return bfs_find_parent(self.root, moves)
    
    def mutate(self):
        choice([self.__expansion_mutation, self.__point_mutation, self.__reduction_mutation])()
    
    def __point_mutation(self):
        co_depth = randint(0, self.depth)
        if co_depth == 0:
            children = self.root.children
            self.root = choice(self.non_terminals)
            self.root.children = children
            
        else:
            bits = [0,1]
            moves = []
            for _ in range(co_depth):
                moves.append(choice(bits))

            parent, child_idx = bfs_find_parent(self.root, moves)
            
            if parent.children[child_idx].is_terminal():
                parent.children[child_idx] = deepcopy(choice(self.terminals))
            
            else:
                children = parent.children[child_idx].children
                parent.children[child_idx] = deepcopy(choice(self.non_terminals))
                parent.children[child_idx].children = children
    
    def __reduction_mutation(self):
        co_depth = randint(1, self.depth-1)
        bits = [0,1]
        moves = []
        for _ in range(co_depth):
            moves.append(choice(bits))
        
        parent, child_idx = bfs_find_parent(self.root, moves)
        parent.children[child_idx] = deepcopy(choice(self.terminals))
    
    def __expansion_mutation(self):
        bits = [0,1]
        moves = []
        for _ in range(self.depth):
            moves.append(choice(bits))
        
        parent, child_idx = bfs_find_parent(self.root, moves)
        parent.children[child_idx], _ = build( parent.depth+1,
                                               self.max_depth,
                                               [full, grow],
                                               self.terminals,
                                               self.non_terminals )
def build( depth,
           max_depth,
           methods: List[int],
           terminals: List[Node],
           non_terminals: List[Node]
        ) -> tuple[Node, int]:

    if depth == max_depth:
        node = deepcopy(choice(terminals))
        node.depth = depth
        print(depth, '|', node.handle)        

        return node, depth
    
    method = choice(methods)

    if method == full or depth == 0:
        node = deepcopy(choice(non_terminals))
    else:
        node = deepcopy(choice(terminals+non_terminals))

    node.depth = depth
    
    print(depth, '|', node.handle)        

    if node.is_terminal():
        return node, depth
    
    tree_depth = depth
    
    for _ in range(2):
        child, child_depth  = build(depth + 1, max_depth, [method],terminals, non_terminals)
        if child_depth > tree_depth:
            tree_depth = child_depth
        node.children.append(child)

    return node, tree_depth
