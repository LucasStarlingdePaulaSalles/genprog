from copy import deepcopy
from math import sqrt
from typing import List
from random import choice, randint
from genprog.modules.gene import *

grow = 0
full = 1

class Chromosome:
    def __init__(self, max_depth: int, methods: List[int], terminals: List[str], non_terminals: List[str]):
        self.terminals: List[str] = terminals
        self.non_terminals: List[str] = non_terminals
        self.max_depth: int = max_depth
        self.depth = -1
        self.root, depth = build(0,randint(1, self.max_depth),methods, terminals, non_terminals)
        self.set_depth(depth)
        self.fenotype: str = '&'
        self.update_fenotype()
        self.fit_val = 0

    def set_depth(self, depth):
        if depth > self.max_depth:
            raise Exception(f'ERR004: invalid depth assingment, depth: {depth} is larger than max depth: {self.max_depth}')
        else:
            if depth > self.depth:
                self.depth = depth

    def update_fenotype(self):
        fen: List[str] = []
        get_fenotype(self.root, fen)
        self.fenotype = ''.join(fen)

    def crossover_choice(self) -> tuple[Gene, int]:
        co_depth = randint(1, self.depth)
        bits = [0,1]
        moves = []
        for _ in range(co_depth):
            moves.append(choice(bits))

        return find_parent(self.root, moves)
    
    def mutate(self):
        mutations = [self.__expansion_mutation, self.__point_mutation]
        if self.depth > 1:
            mutations.append(self.__reduction_mutation)
        choice(mutations)()
    
    def fitness(self, data: List[List[float]], inplace: bool = True):

        sum_squared_err = 0
        for vars in data:
            err = self.root.eval(vars[:-1]) - vars[-1]
            squared_err = err**2
            sum_squared_err += squared_err
        
        mean_squared_err = sum_squared_err / len(data)
        rmse = sqrt(mean_squared_err)
        
        if inplace:
            self.fit_val = rmse

        return rmse
    
    def __point_mutation(self):
        co_depth = randint(0, self.depth)
        if co_depth == 0:
            children = self.root.children
            self.root = get_non_terminal(choice(self.non_terminals))
            self.root.children = children
            
        else:
            bits = [0,1]
            moves = []
            for _ in range(co_depth):
                moves.append(choice(bits))

            parent, child_idx = find_parent(self.root, moves)
            
            if parent.children[child_idx].is_terminal():
                parent.children[child_idx] = get_terminal(choice(self.terminals))
            
            else:
                children = parent.children[child_idx].children
                parent.children[child_idx] = get_non_terminal(choice(self.non_terminals))
                parent.children[child_idx].children = children
    
    def __reduction_mutation(self):
        co_depth = randint(1, self.depth-1)
        bits = [0,1]
        moves = []
        for _ in range(co_depth):
            moves.append(choice(bits))
        
        parent, child_idx = find_parent(self.root, moves)
        parent.children[child_idx] = get_terminal(choice(self.terminals))

        self.set_depth(calc_max_depth(self.root))
    
    def __expansion_mutation(self):
        bits = [0,1]
        moves = []
        for _ in range(self.depth):
            moves.append(choice(bits))
        
        parent, child_idx = find_parent(self.root, moves)
        parent.children[child_idx], new_depth = build( parent.depth+1,
                                               self.max_depth,
                                               [full, grow],
                                               self.terminals,
                                               self.non_terminals )
        
        self.set_depth(new_depth)

def build( depth,
           max_depth,
           methods: List[int],
           terminals: List[str],
           non_terminals: List[str]
        ) -> tuple[Gene, int]:

    if depth > max_depth:
        raise Exception('Building on invalid depth')
    
    if depth == max_depth:
        node = get_terminal(choice(terminals))
        node.depth = depth
        return node, depth
    
    method = choice(methods)

    if method == full or depth == 0:
        node = get_non_terminal(choice(non_terminals))
    else:
        node = get_gene(choice(terminals+non_terminals))

    node.depth = depth

    if node.is_terminal():
        return node, depth
    
    tree_depth = depth
    
    for _ in range(2):
        child, child_depth  = build(depth + 1, max_depth, [method], terminals, non_terminals)
        if child_depth > tree_depth:
            tree_depth = child_depth
        node.children.append(child)

    return node, tree_depth
