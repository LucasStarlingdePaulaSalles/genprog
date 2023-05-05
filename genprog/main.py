from typing import List
from genprog.modules.node import *
from genprog.modules.tree import *

def main():
    terminals = available_terminals(3, [4])
    non_terminals = available_non_terminals()

    tree = Chormossome(2, terminals, non_terminals)
    root = tree.build(0, [full])

    vars = [1.0,2.0,3.0]
    print(vars)
    print(root.eval(vars))

    
if __name__ == '__main__':
    main()
    