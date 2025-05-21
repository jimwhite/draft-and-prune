from z3 import *

# Define variables
member = Array('member', IntSort(), BoolSort())
leader = Int('leader')

solver = Solver()

# Constraints
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)
solver.add(And([Implies(leader == i, member[i]) for i in range(7)]))
solver.add(And([Implies(member[i], leader == i) for i in [0, 1]]))
solver.add(Implies(member[2], member[3]))
solver.add(Implies(member[5], And(Not(member[1]), Not(member[4]))))

# Verma is the leader
solver.add(leader == 4)

# Answer choices
choices = [
    And(Not(member[0]), Not(member[2])),
    And(Not(member[1]), Not(member[3])),
    And(Not(member[2]), Not(member[3])),
    And(Not(member[2]), Not(member[6])),
    And(Not(member[3]), Not(member[5]))
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()