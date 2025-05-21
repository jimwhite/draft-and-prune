from z3 import *

# Define variables
is_member = Array('is_member', IntSort(), BoolSort())
is_leader = Array('is_leader', IntSort(), BoolSort())

solver = Solver()

# Constraints
solver.add(PbEq([(is_member[i], 1) for i in range(7)], 3))  # Constraint 1
solver.add(PbEq([(is_leader[i], 1) for i in range(7)], 1))  # Constraint 2
solver.add(ForAll([i], Implies(is_leader[i], is_member[i]), IntSort()))  # Constraint 3: Fixed: Use IntSort() as the sort argument
# Fixed: Added IntSort() for i
solver.add(ForAll([i], Implies(Or(i == 0, i == 1), Implies(is_member[i], is_leader[i])), IntSort()))  # Constraint 4: Fixed sort
solver.add(Implies(is_member[2], is_member[3]))  # Constraint 5
solver.add(Implies(is_member[5], And(Not(is_member[1]), Not(is_member[4]))))  # Constraint 6

# Taylor is not a member
solver.add(Not(is_member[3]))

# Answer choices
workers = ["Quinn", "Ruiz", "Verma", "Wells", "Xue"]
worker_indices = [0, 1, 4, 5, 6]  # Indices corresponding to the answer choices

for i, worker_index in enumerate(worker_indices):
    solver.push()
    solver.add(Not(is_member[worker_index]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
