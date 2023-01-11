import src.kenken as kenken 
import sys 
import re 
import aima_files.csp

    

if __name__ == "__main__":

    """Read lines from kenken file"""
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        
    f.close()

    kenken_puzzle = kenken.Kenken(lines) 


    if sys.argv[2] == "BT":
        print("Using BT algorithm to solve the puzzle")
        print()
        #kenken.display(csp.backtracking_search(kenken_puzzle), size)   		
    elif sys.argv[2] == "BT+MRV":
        print("Using BT and MRV algorithms to solve the puzzle")
        print()
        #kenken.display(csp.backtracking_search(kenken_puzzle, select_unassigned_variable=csp.mrv), size)
    elif sys.argv[2] == "FC":
        print("Using FC algorithm to solve the puzzle")
        print()
       # kenken.display(csp.backtracking_search(kenken_puzzle, inference=csp.forward_checking), size)
    elif sys.argv[2] == "FC+MRV":        
        print("Using FC and MRV algorithms to solve the puzzle")
        print()
        #kenken.display(csp.backtracking_search(kenken_puzzle, select_unassigned_variable=csp.mrv, inference=csp.forward_checking), size)
    elif sys.argv[2] == "MAC":        
        print("Using MAC algorithm to solve the puzzle")
        print()
        #kenken.display(csp.backtracking_search(kenken_puzzle, inference=csp.mac), size)
    else:
	    print("Error, rerun and hope for the bset")