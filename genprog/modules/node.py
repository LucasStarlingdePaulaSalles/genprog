from typing import List, Callable

class Node:
    def __init__(self):
        self.__unset_type = True
        self.__terminal: bool = False
        self.__var: int = -1
        self.handle: str = ''
        self.__operation: Callable[[List[float]], float] = self.__do_const
        self.__values: List[float] = []
        self.children: List[Node] = []
        self.idx = 0

    def set_type(self, type: bool):
        if not self.__unset_type:
            raise Exception('ERR001: Setting node type for typed node')
        else:
            self.__terminal = type
            self.__unset_type = False
    
    def variable(self, var: int):
        self.set_type(True)
        self.handle = f'x{var}'
        self.__var = var
        self.__operation = self.__do_variable
        return self
    
    def coeficient(self, value: int):
        self.set_type(True)
        self.__values = [float(value)]
        self.handle = f'C{value}'
        return self

    def operator(self, handle: str, operation: Callable[[List[float]],float]):
        self.set_type(False)
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


def available_non_terminals() -> List[Node]:
    def mul(ops: List[float]) -> float:
        return ops.pop(0) * ops.pop(0)
    
    def add(ops: List[float]) -> float:
        return ops.pop(0) + ops.pop(0)
    
    def sub(ops: List[float]) -> float:
        return ops.pop(0) - ops.pop(0)
    
    def div(ops: List[float]) -> float:
        divisor = ops.pop(1)
        if divisor == 0:
            return 100000000.0
        return ops.pop(0) / divisor

    nodes = [
        Node().operator('X', mul),
        Node().operator('+', add),
        Node().operator('-', sub),
        Node().operator('/', div)
    ]
    return nodes


def available_terminals(varc: int, coefs: List[int]) -> List[Node]:
    nodes = []

    for i in range(varc):
        nodes.append(Node().variable(i))
    
    for coef in coefs:
        nodes.append(Node().coeficient(coef))

    return nodes

def bfs(root: Node):
    queue: List[Node] = [] 
    queue.append(root)

    while queue:          
        node = queue.pop(0) 

        print (node.idx, end = " ") 

        for neighbour in node.children:
            queue.append(neighbour)
    
    print()