from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignments: r1[i] = bicycle tested by rider i on day 1
r1 = [Int(f"r1_{i}") for i in range(4)]
# Day 2 assignments: r2[i] = bicycle tested by rider i on day 2
r2 = [Int(f"r2_{i}") for i in range(4)]

solver = Solver()

# Day-wise permutation constraints
for day_assignments in [r1, r2]:
    # Each assignment must be between 0 and 3
    for i in range(4):
        solver.add(day_assignments[i] >= 0, day_assignments[i] <= 3)
    # All assignments distinct
    solver.add(Distinct(*day_assignments))

# State-specific constraints
# Reynaldo cannot test F on day 1: r1[0] != 0
solver.add(r1[0] != 0)

# Yuki cannot test J on day 1: r1[3] != 3
solver.add(r1[3] != 3)

# Theresa must be one of the testers for H (bicycle 2)
solver.add(Or(r1[2] == 2, r2[2] == 2))

# Yuki's day-1 bicycle = Seamus's day-2 bicycle: r1[3] == r2[1]
solver.add(r1[3] == r2[1])

# Answer choices (all refer to day-1 assignments)
answer_choices = [
    # Both Reynaldo and Seamus test J: r1[0] == 3 and r1[1] == 3
    And(r1[0] == 3, r1[1] == 3),
    # Both Reynaldo and Theresa test J: r1[0] == 3 and r1[2] == 3
    And(r1[0] == 3, r1[2] == 3),
    # Both Reynaldo and Yuki test G: r1[0] == 1 and r1[3] == 1
    And(r1[0] == 1, r1[3] == 1),
    # Both Seamus and Theresa test G: r1[1] == 1 and r1[2] == 1
    And(r1[1] == 1, r1[2] == 1),
    # Both Theresa and Yuki test F: r1[2] == 0 and r1[3] == 0
    And(r1[2] == 0, r1[3] == 0)
]

# Check each answer choice
answer_index_list = []
for idx, condition in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the single index that cannot be true
print(answer_index_list[0] if answer_index_list else -1)