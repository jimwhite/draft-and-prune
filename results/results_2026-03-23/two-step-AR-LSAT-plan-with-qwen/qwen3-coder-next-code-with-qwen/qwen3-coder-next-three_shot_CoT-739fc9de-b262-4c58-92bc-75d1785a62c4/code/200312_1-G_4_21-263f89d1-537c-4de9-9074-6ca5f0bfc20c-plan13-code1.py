from z3 import *

# Student indices: 0=Jiang, 1=Kramer, 2=Lopez, 3=Megregian, 4=O'Neill
# Play indices: 0=Sunset, 1=Tamerlane, 2=Undulation

# Boolean variables: rev[i][p] = True if student i reviews play p
rev = [[Bool(f"rev_{i}_{p}") for p in range(3)] for i in range(5)]

# Base solver
solver = Solver()

# Non-empty constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(rev[i][0], rev[i][1], rev[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
count = lambda idx: Sum([If(rev[idx][p], 1, 0) for p in range(3)])
solver.add(count(1) < count(3))  # Kramer < Megregian
solver.add(count(2) < count(3))  # Lopez < Megregian

# Jiang-Lopez/Megregian disjointness: Lopez and Megregian share no plays with Jiang
for p in range(3):
    solver.add(Implies(rev[0][p], And(Not(rev[2][p]), Not(rev[3][p]))))

# Kramer and O'Neill both review Tamerlane
solver.add(rev[1][1] == True)
solver.add(rev[4][1] == True)

# Exactly three students review Undulation (play index 2)
solver.add(Sum([If(rev[i][2], 1, 0) for i in range(5)]) == 3)

# Exactly two students review exactly the same set of plays (one duplicate pair)
# Encode each student's review set as an integer: bit0=Sunset, bit1=Tamerlane, bit2=Undulation
set_val = [Int(f"set_{i}") for i in range(5)]
for i in range(5):
    solver.add(set_val[i] == If(rev[i][0], 1, 0) + 
               If(rev[i][1], 2, 0) + 
               If(rev[i][2], 4, 0))

# Count how many times each set value appears
# We need exactly one pair of identical sets and all others distinct
# So total distinct values = 4, with one value appearing twice

# Create auxiliary variables for counting occurrences of each possible set (0-7)
occ = [Int(f"occ_{v}") for v in range(8)]
for v in range(8):
    solver.add(occ[v] == Sum([If(set_val[i] == v, 1, 0) for i in range(5)]))

# Exactly one value has count == 2, and all others have count == 1
# Since there are 5 students: 2 + 1 + 1 + 1 = 5, so exactly one value appears twice and three values appear once
# This means: sum over v of (occ[v] == 2) == 1, and sum over v of (occ[v] >= 1) == 4

# Count how many values appear at least once
distinct_count = Sum([If(occ[v] >= 1, 1, 0) for v in range(8)])
solver.add(distinct_count == 4)

# Count how many values appear exactly twice
double_count = Sum([If(occ[v] == 2, 1, 0) for v in range(8)])
solver.add(double_count == 1)

# Answer choices
answer_choices = [
    "Megregian does not review Undulation",  # index 0
    "O'Neill does not review Undulation",   # index 1
    "Jiang reviews Undulation",             # index 2
    "Lopez reviews Tamerlane",              # index 3
    "O'Neill reviews Sunset"                # index 4
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # Megregian does not review Undulation
        s_chk.add(Not(rev[3][2]))
    elif idx == 1:  # O'Neill does not review Undulation
        s_chk.add(Not(rev[4][2]))
    elif idx == 2:  # Jiang reviews Undulation
        s_chk.add(rev[0][2])
    elif idx == 3:  # Lopez reviews Tamerlane
        s_chk.add(rev[2][1])
    elif idx == 4:  # O'Neill reviews Sunset
        s_chk.add(rev[4][0])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)