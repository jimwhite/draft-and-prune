from z3 import *

# Variables
is_member = Array('is_member', IntSort(), BoolSort())
is_leader = Array('is_leader', IntSort(), BoolSort())

solver = Solver()

# Constraints
solver.add(PbEq([(is_member[i], 1) for i in range(7)], 3))
solver.add(PbEq([(is_leader[i], 1) for i in range(7)], 1))
i = Int('i')
solver.add(ForAll([i], Implies(is_leader[i], is_member[i])))
solver.add(ForAll([i], Implies(Or(i == 0, i == 1), Implies(is_member[i], is_leader[i]))))
solver.add(Implies(is_member[2], is_member[3]))
solver.add(Implies(is_member[5], And(Not(is_member[1]), Not(is_member[4]))))

# Premise: Taylor is not a member
solver.add(Not(is_member[3]))

# Check answer choices
choices = [0, 1, 4, 5, 6]  # Quinn, Ruiz, Verma, Wells, Xue
option_letter = 'A'
for choice in choices:
    solver.push()
    solver.add(Not(is_member[choice]))
    if solver.check() == unsat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)