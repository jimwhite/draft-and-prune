from z3 import *

# Define variables
is_member = Array('is_member', IntSort(), BoolSort())
is_leader = Array('is_leader', IntSort(), BoolSort())

solver = Solver()

# Constraints
solver.add(PbEq([(is_member[i], 1) for i in range(7)], 3))
solver.add(PbEq([(is_leader[i], 1) for i in range(7)], 1))
i = Int('i') # Declare i before using it in ForAll
solver.add(ForAll(i, Implies(And(0 <= i, i < 7), Implies(is_leader[i], is_member[i])))) # Added range constraint for i
i = Int('i') # Re-declare i for the next ForAll
solver.add(ForAll(i, Implies(And(0 <= i, i < 7), Implies(Or(i == 0, i == 1), Implies(is_member[i], is_leader[i]))))) # Added range constraint for i
solver.add(Implies(is_member[2], is_member[3]))
solver.add(Implies(is_member[5], And(Not(is_member[1]), Not(is_member[4]))))

# Question constraints
solver.add(is_leader[3] == True)
solver.add(is_member[5] == True)

# Check answer choices
options = [
    [0, 2],  # Quinn or Smith
    [0, 6],  # Quinn or Xue
    [1, 4],  # Ruiz or Verma
    [2, 6],  # Smith or Xue
    [4, 6]   # Verma or Xue
]

for option_index, option in enumerate(options):
    solver.push()
    solver.add(Or(And(is_member[option[0]], Not(is_member[option[1]])),
                   And(Not(is_member[option[0]]), is_member[option[1]])))
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
