from z3 import *

# Variables
member = Array('member', IntSort(), BoolSort())
leader = Int('leader')

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3) # Constraint 1
solver.add(And(leader >= 0, leader < 7, member[leader])) # Constraint 2
solver.add(Implies(member[0], leader == 0)) # Constraint 3
solver.add(Implies(member[1], leader == 1)) # Constraint 4
solver.add(Implies(member[2], member[3])) # Constraint 5
solver.add(Implies(member[5], Not(Or(member[1], member[4])))) # Constraint 6

# Verma is leader
solver.add(leader == 4)

# Answer choices
choices = [
    And(Not(member[0]), Not(member[2])), # A
    And(Not(member[1]), Not(member[3])), # B
    And(Not(member[2]), Not(member[3])), # C
    And(Not(member[2]), Not(member[6])), # D
    And(Not(member[3]), Not(member[5]))  # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()