from z3 import *

# Rider indices: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycle indices: 0=F, 1=G, 2=H, 3=J

# r1[i] = bicycle tested by rider i on day 1
# r2[i] = bicycle tested by rider i on day 2
r1 = [Int(f"r1_{i}") for i in range(4)]
r2 = [Int(f"r2_{i}") for i in range(4)]

solver = Solver()

# Domain constraints: each rider tests a bicycle (0-3) on each day
for i in range(4):
    solver.add(r1[i] >= 0, r1[i] <= 3)
    solver.add(r2[i] >= 0, r2[i] <= 3)

# One-per-bicycle-per-day constraints: permutations
solver.add(Distinct(r1))
solver.add(Distinct(r2))

# Conditional constraints:
# Reynaldo cannot test F (bicycle 0) on either day
solver.add(r1[0] != 0)
solver.add(r2[0] != 0)

# Yuki cannot test J (bicycle 3) on either day
solver.add(r1[3] != 3)
solver.add(r2[3] != 3)

# Theresa must test H (bicycle 2) on at least one day
solver.add(Or(r1[2] == 2, r2[2] == 2))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(r2[1] == r1[3])

# Answer choices (EXCEPT means the one that cannot be true)
answer_choices = [
    ("Reynaldo tests J on the first day.", r1[0] == 3),
    ("Reynaldo tests J on the second day.", r2[0] == 3),
    ("Seamus tests H on the first day.", r1[1] == 2),
    ("Yuki tests H on the first day.", r1[3] == 2),
    ("Yuki tests H on the second day.", r2[3] == 2)
]

answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)