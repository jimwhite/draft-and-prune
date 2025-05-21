from z3 import *

# Define variables
member = Array('member', IntSort(), BoolSort())
leader = Int('leader')

# Create solver and add base constraints
solver = Solver()
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)
solver.add(And([Implies(leader == i, member[i]) for i in range(7)]))
solver.add(And(Implies(member[0], leader == 0), Implies(member[1], leader == 1)))
solver.add(Implies(member[2], member[3]))
solver.add(Implies(member[5], And(Not(member[1]), Not(member[4]))))

# Answer choices
choices = [
    And(Not(member[0]), Not(member[2])),
    And(Not(member[0]), Not(member[3])),
    And(Not(member[0]), Not(member[6])),
    And(Not(member[1]), Not(member[5])),
    And(Not(member[1]), Not(member[4]))
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        M = solver.model()
        solver.add(Not(And([member[j] == M.eval(member[j]) for j in range(7)]), leader == M.eval(leader)))
        if solver.check() == unsat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
    solver.pop()