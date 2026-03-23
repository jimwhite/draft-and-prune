from z3 import *

# Rider indices: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycle indices: 0=F, 1=G, 2=H, 3=J

# Day 1 assignments: r1[i] = bicycle tested by rider i on day 1
r1 = [Int(f"r1_{i}") for i in range(4)]
# Day 2 assignments: r2[i] = bicycle tested by rider i on day 2
r2 = [Int(f"r2_{i}") for i in range(4)]

solver = Solver()

# Day-wise permutation constraints
solver.add(Distinct(r1))
solver.add(Distinct(r2))

# Each rider tests a different bicycle on day 2
for i in range(4):
    solver.add(r1[i] != r2[i])

# Explicit condition constraints
# Reynaldo cannot test F (bicycle 0)
solver.add(r1[0] != 0, r2[0] != 0)

# Yuki cannot test J (bicycle 3)
solver.add(r1[3] != 3, r2[3] != 3)

# Theresa must test H (bicycle 2) on at least one day
solver.add(Or(r1[2] == 2, r2[2] == 2))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(r2[1] == r1[3])

# Answer choices (as conjunctions)
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

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)