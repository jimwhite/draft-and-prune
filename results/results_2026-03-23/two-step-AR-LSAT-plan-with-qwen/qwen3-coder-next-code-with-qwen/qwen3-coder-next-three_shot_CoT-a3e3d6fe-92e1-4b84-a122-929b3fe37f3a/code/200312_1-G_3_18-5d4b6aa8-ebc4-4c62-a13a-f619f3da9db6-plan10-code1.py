from z3 import *

# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday

# Batch day variables
o1, o2, o3 = Ints('o1 o2 o3')
p1, p2, p3 = Ints('p1 p2 p3')
s1, s2, s3 = Ints('s1 s2 s3')

# Base solver
solver = Solver()

# Domain constraints: all variables in [0,4]
for var in [o1, o2, o3, p1, p2, p3, s1, s2, s3]:
    solver.add(var >= 0, var <= 4)

# No same-day repeats per cookie type
solver.add(o1 != o2, o2 != o3, o1 != o3)
solver.add(p1 != p2, p2 != p3, p1 != p3)
solver.add(s1 != s2, s2 != s3, s1 != s3)

# Fixed constraint: second sugar batch is Thursday
solver.add(s2 == 3)

# At least one batch on Monday (day 0)
at_least_one_monday = Or(
    o1 == 0, o2 == 0, o3 == 0,
    p1 == 0, p2 == 0, p3 == 0,
    s1 == 0, s2 == 0, s3 == 0
)
solver.add(at_least_one_monday)

# Cross-batch constraint: second oatmeal batch same day as first peanut butter batch
solver.add(o2 == p1)

# Helper function to count batches on a given day
def count_batches(day_var):
    return Sum([If(v == day_var, 1, 0) for v in [o1, o2, o3, p1, p2, p3, s1, s2, s3]])

# Hypothetical condition: there exists a pair of cookie types A != B such that
# A's first batch day = B's third batch day
hypothetical_condition = Or(
    o1 == p3,  # oatmeal first = peanut butter third
    o1 == s3,  # oatmeal first = sugar third
    p1 == o3,  # peanut butter first = oatmeal third
    p1 == s3,  # peanut butter first = sugar third
    s1 == o3,  # sugar first = oatmeal third
    s1 == p3   # sugar first = peanut butter third
)

# Answer choices conditions (as functions of day counts)
def check_A():
    # A: At least one batch on each of the five days
    return And(
        count_batches(0) >= 1,
        count_batches(1) >= 1,
        count_batches(2) >= 1,
        count_batches(3) >= 1,
        count_batches(4) >= 1
    )

def check_B():
    # B: At least two batches on Wednesday (day 2)
    return count_batches(2) >= 2

def check_C():
    # C: Exactly one batch on Monday (day 0)
    return count_batches(0) == 1

def check_D():
    # D: Exactly two batches on Tuesday (day 1)
    return count_batches(1) == 2

def check_E():
    # E: Exactly one batch on Friday (day 4)
    return count_batches(4) == 1

# Collect answer indices where the statement could be false
answer_index_list = []

# For each answer choice, check if its negation is satisfiable under the hypothetical condition
for idx, (check_func, name) in enumerate([
    (check_A, "A"),
    (check_B, "B"),
    (check_C, "C"),
    (check_D, "D"),
    (check_E, "E")
]):
    s_chk = Solver()
    # Add base constraints + hypothetical condition
    s_chk.add(solver.assertions())
    s_chk.add(hypothetical_condition)
    
    # Assert the answer choice is FALSE (negate it)
    s_chk.add(Not(check_func()))
    
    # If SAT, then this choice could be false
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)