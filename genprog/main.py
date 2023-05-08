from typing import List
from genprog.modules.node import *
from genprog.modules.tree import *

def main():
    terminals = available_terminals(3, [4])
    non_terminals = available_non_terminals()
    vars = [1.0,2.0,3.0]

    tree = Chormossome(3, [full], terminals, non_terminals)
    tree2 = Chormossome(3, [full], terminals, non_terminals)

    print_node(tree.root)
    print("---------------------------------------")
    print_node(tree2.root)
    print("---------------------------------------")


    node, idx = tree.crossover_choice()
    node2, idx2 = tree2.crossover_choice()

    aux = node.children[idx]
    node.children[idx] = node2.children[idx2]
    node2.children[idx2] = aux


    print_node(tree.root)
    print("---------------------------------------")
    print_node(tree2.root)
    print("---------------------------------------")

    print(update_depth(node), update_depth(node2))

    
if __name__ == '__main__':
    main()
    