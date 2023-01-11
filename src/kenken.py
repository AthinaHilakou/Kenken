import re
import sys
import aima_files.csp as csp

#sdi: 1115202000213



# ______________________________________________________________________________
# Kenken puzzle 



class Kenken(csp.CSP):

    def __init__(self, lines):
        self.size = int(lines.pop(0))
        self.variables = list()
        self.domains = dict()
        self.neighbors = dict()
        self.clique_variables = dict() #Dictionary of clique index->variables 
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
                self.clique_variables[lines.index(line)].append((grid_line, grid_column))
                self.cliques[(grid_line, grid_column)] = lines.index(line) 
            self.clique_constraint[lines.index(line)] = (target, operand)

        


        csp.CSP().__init__(self, self.variables, self.domains, self.neighbors, self.kenken_constraints)


    def constraint_of_ABteam(self, A, a, B, b):
        clique_members = self.clique_variables[self.cliques[A]] #Get all members of a clique
        members_count = len(clique_members)
        clique_specifics = self.clique_constraints[self.cliques[A]] #Get target, operand tuple
        target = int(clique_specifics[0])
        operand = clique_specifics[1]
        current_assignment = self.infer_assignment()
        clique_value = 0 
        flag = False  
        if (operand == '*'):
            clique_value = a * b
            flag = True 
        elif (operand == '+'):
            clique_value = a + b
            flag = True 
        elif (operand == '-'):
            clique_value = abs(a - b)
        elif (operand == '/'):
            clique_value = max(a,b)/min(a,b)

        assigned_members = 2 
        if(flag == True): #cliques may contain more than two members only if operand = + or *
            clique_members.remove(A)
            clique_members.remove(B)
            for var in clique_members: 
                if var in current_assignment.keys():
                    assigned_members = assigned_members + 1
                    if (operand == '*'):
                        clique_value = clique_value*current_assignment[var]
                    elif (operand == '+'):
                        clique_value = clique_value + current_assignment[var]
        
        if ((members_count > assigned_members) and (target > clique_value)):
            return True
        elif ((members_count == assigned_members) and (target == clique_value)):
            return True  
        return False 
    
    def constraint_of_Ateam(self, A , a):
        clique_members = self.clique_variables[self.cliques[A]] #Get all members of a clique
        members_count = len(clique_members)
        clique_specifics = self.clique_constraints[self.cliques[A]] #Get target, operand tuple
        target = int(clique_specifics[0])
        operand = clique_specifics[1]
        current_assignment = self.infer_assignment()
        clique_value = a 
        assigned_members = 1
        clique_members.remove(A)
        for var in clique_members: 
            if var in current_assignment.keys():
                assigned_members = assigned_members + 1
                if (operand == '*'):
                    clique_value = clique_value*current_assignment[var]
                elif (operand == '+'):
                    clique_value = clique_value + current_assignment[var]
                elif (operand == '-'):
                    clique_value = abs(clique_value - current_assignment[var])
                elif (operand == '/'):
                    clique_value = max(clique_value,current_assignment[var])/min(clique_value, current_assignment[var])
        if len(clique_members) == 0: #Clique consists of one member only, operand is = 
            return (a == target)
          
        if ((members_count > assigned_members) and (target > clique_value)):
            return True
        elif ((members_count == assigned_members) and (target == clique_value)):
            return True  
        return False 



     
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

