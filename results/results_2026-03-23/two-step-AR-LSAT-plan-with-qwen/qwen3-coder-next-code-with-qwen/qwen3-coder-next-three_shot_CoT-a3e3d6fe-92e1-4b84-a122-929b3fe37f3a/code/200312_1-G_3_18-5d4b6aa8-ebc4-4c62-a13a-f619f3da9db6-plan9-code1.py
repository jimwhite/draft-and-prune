from z3 import *

# Cookie types: 0-oatmeal, 1-peanut butter, 2-sugar
# Days: 1-Monday, 2-Tuesday, 3-Wednesday, 4-Thursday, 5-Friday

# Create variables: batch_type_day[type][batch_num] where batch_num is 1,2,3
batch = [[Int(f"b_{t}_{b}") for b in range(1, 4)] for t in range(3)]

solver = Solver()

# Domain constraints: each batch day between 1 and 5
for t in range(3):
    for b in range(3):
        solver.add(batch[t][b] >= 1, batch[t][b] <= 5)

# Distinct-day-per-type constraint: strictly increasing days for each cookie type
for t in range(3):
    solver.add(batch[t][0] < batch[t][1], batch[t][1] < batch[t][2])

# Monday at least one batch
solver.add(Or(*[batch[t][b] == 1 for t in range(3) for b in range(3)]))

# Given relative constraints:
# Second oatmeal batch = first peanut butter batch
solver.add(batch[0][1] == batch[1][0])
# Second sugar batch = Thursday (day 4)
solver.add(batch[2][1] == 4)

# Conditional premise: there exists X != Y such that first batch of X = third batch of Y
aux = [Bool(f"aux_{i}") for i in range(6)]
solver.add(
    Or(
        And(aux[0], batch[0][0] == batch[1][2]),
        And(aux[1], batch[0][0] == batch[2][2]),
        And(aux[2], batch[1][0] == batch[0][2]),
        And(aux[3], batch[1][0] == batch[2][2]),
        And(aux[4], batch[2][0] == batch[0][2]),
        And(aux[5], batch[2][0] == batch[1][2])
    )
)

# Answer choices (statements that could be false)
answer_choices = [
    # 0: At least one batch on each of the five days
    lambda: And(*[Or(*[batch[t][b] == d for t in range(3) for b in range(3)]) for d in range(1, 6)]),
    # 1: At least two batches on Wednesday (day 3)
    lambda: Sum([If(batch[t][b] == 3, 1, 0) for t in range(3) for b in range(3)]) >= 2,
    # 2: Exactly one batch on Monday (day 1)
    lambda: Sum([If(batch[t][b] == 1, 1, 0) for t in range(3) for b in range(3)]) == 1,
    # 3: Exactly two batches on Tuesday (day 2)
    lambda: Sum([If(batch[t][b] == 2, 1, 0) for t in range(3) for b in range(3)]) == 2,
    # 4: Exactly one batch on Friday (day 5)
    lambda: Sum([If(batch[t][b] == 5, 1, 0) for t in range(3) for b in range(3)]) == 1
]

# Check each answer choice: if negation is satisfiable, then the statement could be false
answer_index_list = []
for idx, stmt in enumerate(answer_choices):
    s_chk = Solver()
    # Add base constraints + premise
    s_chk.add(solver.assertions())
    
    # Add negation of the statement
    s_chk.add(Not(stmt()))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)