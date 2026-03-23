from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{s}_{p}") for p in range(3)] for s in range(5)]

solver = Solver()

# Non-empty review constraint: each student reviews at least one play
for s in range(5):
    solver.add(Or(review[s][0], review[s][1], review[s][2]))

# Kramer and Lopez each review fewer plays than Megregian
count = lambda s: Sum([If(review[s][p], 1, 0) for p in range(3)])
solver.add(count(1) < count(3))  # Kramer < Megregian
solver.add(count(2) < count(3))  # Lopez < Megregian

# Jiang–Lopez/Megregian disjointness constraint
for p in range(3):
    solver.add(Implies(review[0][p], And(Not(review[2][p]), Not(review[3][p]))))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two of the students review exactly the same play or plays as each other
# We need to enforce: there exists a pair (s1, s2) with identical review sets,
# and all other students have different review sets from this pair.

# Create auxiliary boolean variables for each possible pair being identical
pair_identical = []
for s1 in range(5):
    for s2 in range(s1 + 1, 5):
        identical = And(*[review[s1][p] == review[s2][p] for p in range(3)])
        pair_identical.append((s1, s2, identical))

# At least one pair is identical
solver.add(Or([ident for _, _, ident in pair_identical]))

# For each pair that is identical, ensure no third student has the same set
for s1, s2, ident in pair_identical:
    for s3 in range(5):
        if s3 != s1 and s3 != s2:
            # If s1 and s2 are identical, then s3 must differ from them
            solver.add(Implies(ident, Or([review[s1][p] != review[s3][p] for p in range(3)])))

# Hypothesis: exactly three students review Undulation
solver.add(Sum([If(review[s][2], 1, 0) for s in range(5)]) == 3)

# Answer choices
answer_choices = [
    "Megregian does not review Undulation.",  # index 0
    "O'Neill does not review Undulation.",   # index 1
    "Jiang reviews Undulation.",             # index 2
    "Lopez reviews Tamerlane.",              # index 3
    "O'Neill reviews Sunset."                # index 4
]

# Check each answer choice
satisfiable_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # Megregian does not review Undulation
        s_chk.add(Not(review[3][2]))
    elif idx == 1:  # O'Neill does not review Undulation
        s_chk.add(Not(review[4][2]))
    elif idx == 2:  # Jiang reviews Undulation
        s_chk.add(review[0][2])
    elif idx == 3:  # Lopez reviews Tamerlane
        s_chk.add(review[2][1])
    elif idx == 4:  # O'Neill reviews Sunset
        s_chk.add(review[4][0])
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

print(satisfiable_indices)