from z3 import *

# Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Batches: 1, 2, 3

x = {}
for d in range(1, 6):
    for t in range(3):
        for k in range(1, 4):
            x[(d, t, k)] = Bool(f"x_{d}_{t}_{k}")

solver = Solver()

# Exactly one day per (cookie type, batch)
for t in range(3):
    for k in range(1, 4):
        solver.add(Or([x[(d, t, k)] for d in range(1, 6)]))
        for d1 in range(1, 6):
            for d2 in range(d1 + 1, 6):
                solver.add(Not(And(x[(d1, t, k)], x[(d2, t, k)])))

# No two batches of same type on same day
for d in range(1, 6):
    for t in range(3):
        for k1 in range(1, 4):
            for k2 in range(k1 + 1, 4):
                solver.add(Not(And(x[(d, t, k1)], x[(d, t, k2)])))

# At least one batch on Monday
solver.add(Or([x[(1, t, k)] for t in range(3) for k in range(1, 4)]))

# Second oatmeal = first peanut butter
for d in range(1, 6):
    solver.add(Or(Not(x[(d, 0, 2)]), x[(d, 1, 1)]))
    solver.add(Or(Not(x[(d, 1, 1)]), x[(d, 0, 2)]))

# Second sugar on Thursday
solver.add(x[(4, 2, 2)])

# Premise: exists d, t1 != t2 such that x[d][t1][1] and x[d][t2][3]
premise_vars = []
for d in range(1, 6):
    for t1 in range(3):
        for t2 in range(3):
            if t1 != t2:
                premise_vars.append(Bool(f"premise_{d}_{t1}_{t2}"))
                solver.add(Implies(premise_vars[-1], And(x[(d, t1, 1)], x[(d, t2, 3)])))
solver.add(Or(premise_vars))

# Helper: count batches on day d
def count_batches(d):
    return Sum([If(x[(d, t, k)], 1, 0) for t in range(3) for k in range(1, 4)])

# Answer choices (negations to test if they could be false)
answer_negations = []

# A: At least one batch per day -> negation: exists a day with 0 batches
day_zero = []
for d in range(1, 6):
    day_zero.append(count_batches(d) == 0)
answer_negations.append(Or(day_zero))

# B: At least two batches on Wednesday (day 3) -> negation: <=1 batch
answer_negations.append(count_batches(3) < 2)

# C: Exactly one batch on Monday (day 1) -> negation: !=1, i.e., >=2
answer_negations.append(count_batches(1) > 1)

# D: Exactly two batches on Tuesday (day 2) -> negation: !=2, i.e., <=1 or >=3
answer_negations.append(Or(count_batches(2) < 2, count_batches(2) > 2))

# E: Exactly one batch on Friday (day 5) -> negation: !=1, i.e., >=2
answer_negations.append(count_batches(5) > 1)

# Check each answer choice
answer_index_list = []
for idx, neg in enumerate(answer_negations):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(neg)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)