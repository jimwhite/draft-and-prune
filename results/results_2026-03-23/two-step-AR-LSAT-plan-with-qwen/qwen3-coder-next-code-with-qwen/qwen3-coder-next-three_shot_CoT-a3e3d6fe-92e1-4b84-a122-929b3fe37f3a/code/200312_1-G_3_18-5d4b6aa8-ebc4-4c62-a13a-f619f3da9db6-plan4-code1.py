from z3 import *

# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri

# Batch variables: o[0], o[1], o[2] for oatmeal (first, second, third)
o = [Int(f"o_{i}") for i in range(3)]
p = [Int(f"p_{i}") for i in range(3)]
s = [Int(f"s_{i}") for i in range(3)]

# Base solver
solver = Solver()

# Domain constraints: all batch days between 0 and 4
for var_list in [o, p, s]:
    for v in var_list:
        solver.add(v >= 0, v <= 4)

# Distinctness per type: no two batches of same cookie on same day
for var_list in [o, p, s]:
    solver.add(Distinct(*var_list))

# At least one batch on Monday (day 0)
all_batches = o + p + s
solver.add(Or(*[b == 0 for b in all_batches]))

# Second sugar batch is Thursday (day 4)
solver.add(s[1] == 4)

# Second oatmeal batch = first peanut butter batch
solver.add(o[1] == p[0])

# Hypothesis: there exists a pair where A's first batch = B's third batch
# Consider all ordered pairs of distinct types: (o,p), (o,s), (p,o), (p,s), (s,o), (s,p)
hypothesis = Or(
    o[0] == p[2],
    o[0] == s[2],
    p[0] == o[2],
    p[0] == s[2],
    s[0] == o[2],
    s[0] == p[2]
)

# Add hypothesis to solver
solver.add(hypothesis)

# Answer options as functions that return expressions for each option
def count_on_day(day_val):
    return Sum([If(b == day_val, 1, 0) for b in all_batches])

# Option expressions
option_exprs = [
    # Option 0: At least one batch on each of the five days
    And(*[count_on_day(d) >= 1 for d in range(5)]),
    
    # Option 1: At least two batches on Wednesday (day=2)
    count_on_day(2) >= 2,
    
    # Option 2: Exactly one batch on Monday (day=0)
    count_on_day(0) == 1,
    
    # Option 3: Exactly two batches on Tuesday (day=1)
    count_on_day(1) == 2,
    
    # Option 4: Exactly one batch on Friday (day=4)
    count_on_day(4) == 1
]

# Check which options could be false under the hypothesis
answer_index_list = []
for idx, opt_expr in enumerate(option_exprs):
    # Check if option can be false while satisfying base + hypothesis
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(Not(opt_expr))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)