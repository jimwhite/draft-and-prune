from z3 import *

# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday

# Create variables: batch_day[type][batch] where type in {0,1,2}, batch in {0,1,2}
batch_day = [[Int(f"bd_{t}_{b}") for b in range(3)] for t in range(3)]

solver = Solver()

# Domain constraints: each batch day is between 0 and 4
for t in range(3):
    for b in range(3):
        solver.add(batch_day[t][b] >= 0, batch_day[t][b] <= 4)

# Distinct-day-per-type constraint: batches of same type on different days
for t in range(3):
    solver.add(
        batch_day[t][0] != batch_day[t][1],
        batch_day[t][0] != batch_day[t][2],
        batch_day[t][1] != batch_day[t][2]
    )

# At least one batch on Monday (day 0)
solver.add(Or(*[batch_day[t][b] == 0 for t in range(3) for b in range(3)]))

# Oatmeal second batch same day as peanut butter first batch
solver.add(batch_day[0][1] == batch_day[1][0])

# Sugar second batch on Thursday (day 3)
solver.add(batch_day[2][1] == 3)

# Count variables per day: count[d] = number of batches on day d
count = [Int(f"count_{d}") for d in range(5)]
for d in range(5):
    solver.add(count[d] == Sum([If(batch_day[t][b] == d, 1, 0) for t in range(3) for b in range(3)]))

# Conditional scenario: there exists a day where one kind's first batch coincides with another kind's third batch
# i.e., exists t1 != t2, day d such that batch_day[t1][0] == d and batch_day[t2][2] == d
# We'll encode this as a disjunction of all possible such equalities

conditional_assertions = []
for t1 in range(3):
    for t2 in range(3):
        if t1 != t2:
            for d in range(5):
                conditional_assertions.append(
                    And(batch_day[t1][0] == d, batch_day[t2][2] == d)
                )

# Create solver for conditional scenario
solver_cond = Solver()
solver_cond.add(solver.assertions())
solver_cond.add(Or(*conditional_assertions))

# Answer choices (indices 0-4)
# A: At least one batch on each day -> all(count[d] >= 1 for d in 0..4)
# B: At least two batches on Wednesday (day 2) -> count[2] >= 2
# C: Exactly one batch on Monday (day 0) -> count[0] == 1
# D: Exactly two batches on Tuesday (day 1) -> count[1] == 2
# E: Exactly one batch on Friday (day 4) -> count[4] == 1

# For each choice, check if it could be false under the conditional scenario
answer_index_list = []

# Choice A: At least one batch on each day (negation: some day has 0 batches)
s_A = Solver()
s_A.add(solver_cond.assertions())
# Negation: exists day d such that count[d] == 0
s_A.add(Or(*[count[d] == 0 for d in range(5)]))
if s_A.check() == sat:
    answer_index_list.append(0)

# Choice B: At least two batches on Wednesday (negation: count[2] < 2)
s_B = Solver()
s_B.add(solver_cond.assertions())
s_B.add(count[2] < 2)
if s_B.check() == sat:
    answer_index_list.append(1)

# Choice C: Exactly one batch on Monday (negation: count[0] != 1)
s_C = Solver()
s_C.add(solver_cond.assertions())
s_C.add(count[0] != 1)
if s_C.check() == sat:
    answer_index_list.append(2)

# Choice D: Exactly two batches on Tuesday (negation: count[1] != 2)
s_D = Solver()
s_D.add(solver_cond.assertions())
s_D.add(count[1] != 2)
if s_D.check() == sat:
    answer_index_list.append(3)

# Choice E: Exactly one batch on Friday (negation: count[4] != 1)
s_E = Solver()
s_E.add(solver_cond.assertions())
s_E.add(count[4] != 1)
if s_E.check() == sat:
    answer_index_list.append(4)

print(answer_index_list)