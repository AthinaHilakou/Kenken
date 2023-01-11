import src.kenken as kenken 
import sys 
import re 


    

if __name__ == "__main__":

    """Read lines from kenken file"""
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        
    f.close()

    kenken_puzzle = Kenken(lines) 