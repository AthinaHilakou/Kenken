import re
import sys
import aima_files.csp

#sdi: 1115202000213



# ______________________________________________________________________________
# Kenken puzzle 



class Kenken(CSP):

    def __init__(self, lines):
        self.size = int(lines.pop(0))
        self.variables = list()
        self.domains = dict()
        self.neighbors = dict()
        self.cliques = dict() #A dictionary of variable->clique index, clique index is unique for each clique
        self.clique_constraints = dict() #A dictionary of clique index -> clique constraint
        #Constraints are of type (int, 'operand'), where int, operand denote the target result of the clique and the operand used for the 
        # constaint accordingly 




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
            clique_vars = vars.split('-')
            for c_var in clique_vars:
                grid_line = int(c_var)/self.size
                grid_column = int(c_var)%self.size
                self.cliques[(grid_line, grid_column)] = lines.index(line) 
            self.clique_constraint[lines.index(line)] = (target, operand)

        


        CSP().__init__(self, self.variables, self.domains, self.neighbors,self.kenken_constraints)


    def constraint_of_ABteam(self, A, a, B, b):
        if self.cliques[A] != self.cliques[B]:
            return False
        else: 
            constraint = self.clique_constraints[self.cliques[A]]
            constraint[0] #target 
            constraint[1] #operand
        return 
    
    def constraint_of_Ateam(A , a):
        
        return 
     
    def kenken_constraints(self, A, a, B, b):
        if A[0] == B[0] or A[1] == B[1]:
            if a == b:
                return False
        if self.cliques[A] == self.cliques[B]:
            res = self.constraint_of_ABteam(A, a, B, b)
        else:
            res = (self.constraint_of_Ateam(A, a) and self.constraint_of_Ateam(B, b))
       
        return res 




   
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


