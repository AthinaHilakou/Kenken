import re
import sys
import csp

#sdi: 1115202000213



# ______________________________________________________________________________
# Kenken puzzle 



class Kenken(csp.CSP):

    def __init__(self, lines):
        self.size = int(lines.pop(0))
        self.variables = list()
        self.domains = dict()
        self.neighbors = dict()
        self.clique_variables = dict() #Dictionary of clique index->variables, , clique index is unique for each clique
        self.cliques = dict() #Dictionary of variable->clique index
        self.clique_constraints = dict() #Dictionary of clique index -> clique constraint
        #Constraints are of type (int, 'operand'), where int, operand denote the target result of the clique and the operand used 




        """Variables for Kenken, 0-based indexing"""
        for i in range(self.size): 
            for j in range(self.size):
                self.variables.append((i,j))

        """Domains for Kenken"""
        for var in self.variables:
            self.domains[var] = [i for i in range(1, self.size + 1)]
        #UniversalDict(range(1, self.size + 1))

        """Neighbors for Kenken"""
        for var in self.variables: 
            self.neighbors[var] = []
            for i in range(self.size):
                if i != var[0]:
                    self.neighbors[var].append((i, var[1]))
            for i in range(self.size):
                if i != var[1]:
                    self.neighbors[var].append((var[0], i))

            
            

        """Parse Lines"""
        for line in lines:
            target, vars, operand = line.split('#')
            operand = operand.replace('\n','')
            clique_vars = vars.split('-')
            self.clique_variables[lines.index(line)] = list()
            for c_var in clique_vars:
                grid_line = int(int(c_var)/self.size)
                grid_column = int(int(c_var)%self.size)
                self.clique_variables[lines.index(line)].append((grid_line, grid_column))
                self.cliques[(grid_line, grid_column)] = lines.index(line) 
            self.clique_constraints[lines.index(line)] = (target, operand)

        


        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.kenken_constraints)




    def constraint_of_ABteam(self, A, a, B, b):
        clique_members = self.clique_variables[self.cliques[A]].copy() #Get a copy of members of A's and B's clique
        members_count = len(clique_members)
        clique_specifics = self.clique_constraints[self.cliques[A]] #Get target, operand tuple
        target = int(clique_specifics[0])
        operand = clique_specifics[1]
        current_assignment = self.infer_assignment()
        clique_value = 0 
        assigned_members = 2 
        
        clique_members.remove(A) #So that we don't count them twice
        clique_members.remove(B)
        
        if (operand == '='): #Equality 
            return ((a == b) and (a == target) and (A == B))
        
        elif (operand == '*'): #Multiplication 
            clique_value = a * b
            for var in clique_members: 
                if var in current_assignment:
                    assigned_members += 1
                    clique_value *= current_assignment[var]
            if (members_count > assigned_members): 
                return (target >= clique_value) 
            elif (members_count == assigned_members):
                return (target == clique_value) 
        
        elif (operand == '+'):
            clique_value = a + b
            for var in clique_members: 
                if var in current_assignment:
                    assigned_members += 1
                    clique_value += current_assignment[var]
            if (members_count > assigned_members): 
                return (target > clique_value)
            elif (members_count == assigned_members):
                return (target == clique_value)  

        elif (operand == '-'):
            clique_value = abs(a - b) 
            return (clique_value == target)
        
        elif (operand == '/'):
            clique_value = max(a,b)/min(a,b)
            return (clique_value == target)

        
     
    
    
    
    def constraint_of_Ateam(self, A , a):
        clique_members = self.clique_variables[self.cliques[A]].copy() #Get a copy of members of A's clique
        members_count = len(clique_members)
        clique_specifics = self.clique_constraints[self.cliques[A]] #Get target, operand tuple
        target = int(clique_specifics[0])
        operand = clique_specifics[1]
        current_assignment = self.infer_assignment() # Variables currently assigned 
        clique_value = a   # Initialize clique's value = A's value 
        assigned_members = 1 #Clique's members currently assigned a value (that we know of)
        
        
        
        clique_members.remove(A) # So that we don't count it twice 
        
        if (operand == '='): #Equality 
            return (a == target)  
        
        elif (operand == '*'): #Multiplication
            for var in clique_members:
                if var in current_assignment:
                    assigned_members += 1
                    clique_value *= current_assignment[var]
            if (members_count > assigned_members): 
                return (target >= clique_value) 
            elif (members_count == assigned_members):
                return (target == clique_value) 


        elif (operand == '+'): #Addition
            for var in clique_members:
                if var in current_assignment:
                    assigned_members += 1
                    clique_value += current_assignment[var]
            if (members_count > assigned_members): 
                return (target > clique_value)
            elif (members_count == assigned_members):
                return (target == clique_value)  
            
                    
        elif (operand == '-'): #Subtraction 
            for var in clique_members: 
                if var in current_assignment:
                    assigned_members += 1
                    clique_value = abs(clique_value - current_assignment[var])
            if (members_count > assigned_members):  
                return (target != clique_value)
            elif (members_count == assigned_members):
                return (target == clique_value)   

        
        
        elif (operand == '/'): #Division 
            for var in clique_members: 
                if var in current_assignment:
                    assigned_members += 1
                    clique_value = max(clique_value,current_assignment[var])/min(clique_value, current_assignment[var])
            if (members_count > assigned_members):  
                return (target >= clique_value)
            elif (members_count == assigned_members):
                return (target == clique_value) 

        

     
    def kenken_constraints(self, A, a, B, b):
        if A[0] == B[0] or A[1] == B[1]: # A != B 
            if a == b:
                return False
        
        for n in self.neighbors[A]: # A must have different value from all neighboring variables
            if n in self.infer_assignment() and self.infer_assignment()[n] == a:
                return False
    
        for n in self.neighbors[B]: # B must have different value from all neighboring variables
            if n in self.infer_assignment() and self.infer_assignment()[n] == b:
                return False
        
        
        if self.cliques[A] == self.cliques[B]:
            res = self.constraint_of_ABteam(A, a, B, b)
        else:
            res = (self.constraint_of_Ateam(A, a) and self.constraint_of_Ateam(B, b))
        
        return res 


    def display(self, assignment):
        if (assignment == None):
            print("No solution was found")
        
        else:
            for i in range(self.size):
                for j in range(self.size):
                    z = int(assignment[(i, j)])
                    print(z, end = ' ')
                print('\n')
        return


   
# ______________________________________________________________________________
#Inputs 
"""
Kenken Board Size

Target#CliqueParticipants#Operation

Target#CliqueParticipants#Operation

Target#CliqueParticipants#Operation

...

Target#CliqueParticipants#Operation

Target : Target number of each clique 

CliqueParticipants : Cells that participate in each clique 

Operation : Operator of each clique 
"""




if __name__ == "__main__":
    print(sys.argv[1])
    """Read lines from kenken file"""
    with open(sys.argv[1], 'r') as f:
       lines = f.readlines()
    
    f.close()

    kenken_puzzle = Kenken(lines)
    #for i in range(1 ,1000):
    #   for j in range(1, 1000):
    #      if  kenken_puzzle.kenken_constraints((0,0), i, (2,2), j):
    #            print(i == 3 and j < 7)

    #print(kenken_puzzle.size)
    #print(kenken_puzzle.clique_constraints)
    #print(kenken_puzzle.clique_variables)
    #print(kenken_puzzle.cliques)
    #print()
    #print(kenken_puzzle.domains)
    #print()
    #print(kenken_puzzle.variables)
    #print()
    #print(kenken_puzzle.neighbors)

    if sys.argv[2] == "BT":
        print("Using BT algorithm to solve the puzzle")
        print()
        kenken_puzzle.display(csp.backtracking_search(kenken_puzzle))   		
    elif sys.argv[2] == "BT+MRV":
        print("Using BT and MRV algorithms to solve the puzzle")
        print()
        kenken_puzzle.display(csp.backtracking_search(kenken_puzzle, select_unassigned_variable=csp.mrv))
    elif sys.argv[2] == "FC":
        print("Using FC algorithm to solve the puzzle")
        print()
        kenken_puzzle.display(csp.backtracking_search(kenken_puzzle, inference=csp.forward_checking))
    elif sys.argv[2] == "FC+MRV":        
        print("Using FC and MRV algorithms to solve the puzzle")
        print()
        kenken_puzzle.display(csp.backtracking_search(kenken_puzzle, select_unassigned_variable=csp.mrv, inference=csp.forward_checking))
    elif sys.argv[2] == "MAC":        
        print("Using MAC algorithm to solve the puzzle")
        print()
        kenken_puzzle.display(csp.backtracking_search(kenken_puzzle, inference=csp.mac))
    else:
	    print("Error, rerun and hope for the bset")


