from typing import List, Callable
from math import inf 

class Gene:
    def __init__(self):
        self.depth = 0
        self.handle: str = ''
        self.children: List[Gene] = []
        self.__unset_type = True
        self.__terminal: bool = False
        self.__var: int = -1
        self.__operation: Callable[[List[float]], float] = self.__do_const
        self.__values: List[float] = []

    def set_terminal(self, type: bool):
        if not self.__unset_type:
            raise Exception('ERR001: Setting node type for typed node')
        else:
            self.__terminal = type
            self.__unset_type = False
    
    def variable(self, var: int):
        self.set_terminal(True)
        self.handle = f'x{var}'
        self.__var = var
        self.__operation = self.__do_variable
        return self
    
    def coeficient(self, value: int):
        self.set_terminal(True)
        self.__values = [float(value)]
        self.handle = f'C{value}'
        return self

    def operator(self, handle: str, operation: Callable[[List[float]],float]):
        self.set_terminal(False)
        self.handle = handle
        self.__operation = operation
        return self

    def eval(self, vars: List[float]) -> float:
        if self.__unset_type:
            raise Exception('ERR002: Tring to resolve unset node')
        
        if not self.__terminal:
            for child in self.children:
                step = child.eval(vars)
                self.__values.append(step)

            return self.__operation(self.__values)
        else:
            return self.__operation(vars)


    def __do_variable(self, vars: List[float]) -> float:
        return vars[self.__var]
    
    def __do_const(self, _: List[float]) -> float:
        return self.__values[0]
    
    def is_terminal(self) -> bool:
        return self.__terminal


def mul(ops: List[float]) -> float:
    return ops.pop(0) * ops.pop(0)

def add(ops: List[float]) -> float:
    return ops.pop(0) + ops.pop(0)

def sub(ops: List[float]) -> float:
    return ops.pop(0) - ops.pop(0)

def div(ops: List[float]) -> float:
    divisor = ops.pop(1)
    if divisor == 0:
        return 10000
    return ops.pop(0) / divisor

def available_non_terminals() -> List[str]:
    options = ['*','+','-','/']
    return options

def get_non_terminal(handle: str) -> Gene:
    if handle == '*':
        return Gene().operator('*', mul)
    elif handle == '+':
        return Gene().operator('+', add)
    elif handle == '-':
        return Gene().operator('-', sub)
    elif handle == '/':
        return Gene().operator('/', div)
    else:
        raise Exception('ERR003: Invalid non terminal handle')

def available_terminals(varc: int, coefs: List[int] = []) -> List[str]:
    options = []

    for i in range(varc):
        options.append(f'x{i}')
    
    for coef in coefs:
        options.append(f'C{coef}')

    return options

def get_terminal(handle: str) -> Gene:

    if handle[0] == 'x':
        return Gene().variable(int(handle[1:]))
    elif handle[0] == 'C':
        return Gene().coeficient(int(handle[1:]))
    else:
        raise Exception('ERR004: invalid terminal handle')

def get_gene(handle: str) -> Gene:
    if handle[0] == 'x' or handle[0] == 'C':
        return get_terminal(handle)
    else: 
        return get_non_terminal(handle) 

def find_parent(root: Gene, moves: List[int]) -> tuple[Gene, int]:
    while len(moves) > 1:          
        move = moves.pop(0)

        if root.children[move].is_terminal():
            return root, move
        
        root = root.children[move]

    move = moves.pop(0)
    return root, move

def print_node(root: Gene):
    queue: List[Gene] = [] 
    queue.append(root)
    depth = root.depth
    count = 0

    while queue:          
        node = queue.pop(0) 
        if node.depth > depth:
            print()
            depth = node.depth
            count = 0
        
        if count == 2:
            print("|", end= " ")
            count = 0
        print (node.handle, end = " ") 
        count += 1
        for child in node.children:
            child.depth = depth + 1
            queue.append(child)
    
    print()

def calc_max_depth(root: Gene) -> int:
    queue: List[Gene] = [] 
    queue.append(root)
    depth = root.depth

    while queue:
        node = queue.pop(0) 
        if node.depth > depth:
            depth = node.depth
        
        for child in node.children:
            child.depth = depth + 1
            queue.append(child)
    
    return depth

def print_infix(root: Gene):
    terminal = len(root.children) == 0

    if not terminal:
        
        if not root.children[0].is_terminal(): print('(', end='')
        print_infix(root.children[0])
        if not root.children[0].is_terminal(): print(')', end='')

    print(root.handle, end='')

    if not terminal:
        if not root.children[1].is_terminal(): print('(', end='')
        print_infix(root.children[1])
        if not root.children[1].is_terminal(): print(')', end='')

def get_fenotype(root: Gene, fenotype: List[str]):
    terminal = len(root.children) == 0

    if not terminal:
        
        if not root.children[0].is_terminal(): fenotype += '('
        get_fenotype(root.children[0], fenotype)
        if not root.children[0].is_terminal(): fenotype += ')'

    fenotype += root.handle

    if not terminal:
        if not root.children[1].is_terminal(): fenotype += '('
        get_fenotype(root.children[1], fenotype)
        if not root.children[1].is_terminal(): fenotype += ')'
