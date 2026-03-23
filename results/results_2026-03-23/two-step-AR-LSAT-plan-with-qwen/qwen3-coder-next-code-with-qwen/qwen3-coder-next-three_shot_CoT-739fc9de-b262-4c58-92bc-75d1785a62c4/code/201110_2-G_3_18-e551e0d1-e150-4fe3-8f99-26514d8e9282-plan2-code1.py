from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 and Day 2 assignment variables
d1 = [[Bool(f"d1_{r}_{b}") for b in range(4)] for r in range(4)]
d2 = [[Bool(f"d2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for r in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for r in range(4)]) == 1)

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for r in range(4):
    solver.add(Sum([If(d2[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(d2[r][b], 1, 0) for r in range(4)]) == 1)

# Global constraints
# Reynaldo cannot test F on either day
solver.add(Not(d1[0][0]), Not(d2[0][0]))

# Yuki cannot test J on either day
solver.add(Not(d1[3][3]), Not(d2[3][3]))

# Theresa must test H on at least one day
solver.add(Or(d1[2][2], d2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(d1[3][b], d2[1][b]))

# Answer choices: each is a claim about day 1 assignments
answer_choices = [
    # Both Reynaldo and Seamus test J (day 1)
    And(d1[0][3], d1[1][3]),
    # Both Reynaldo and Theresa test J (day 1)
    And(d1[0][3], d1[2][3]),
    # Both Reynaldo and Yuki test G (day 1)
    And(d1[0][1], d1[3][1]),
    # Both Seamus and Theresa test G (day 1)
    And(d1[1][1], d1[2][1]),
    # Both Theresa and Yuki test F (day 1)
    And(d1[2][0], d1[3][0])
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific claim
    s_chk.add(choice)
    
    # If UNSAT, this claim cannot be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Print the index of the choice that CANNOT be true
print(answer_index_list[0] if answer_index_list else -1)