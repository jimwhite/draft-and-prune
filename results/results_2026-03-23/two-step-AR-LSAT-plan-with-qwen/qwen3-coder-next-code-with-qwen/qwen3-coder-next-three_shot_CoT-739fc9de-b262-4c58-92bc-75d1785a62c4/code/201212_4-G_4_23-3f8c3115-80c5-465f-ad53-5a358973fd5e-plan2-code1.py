from z3 import *

# Article indices: 0=G, 1=H, 2=J (finance); 3=Q, 4=R, 5=S (nutrition); 6=Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topics = [0, 0, 0, 1, 1, 1, 2]  # 0=finance, 1=nutrition, 2=wildlife

# Position variables: pos[i] = position of article i (1 to 7)
pos = [Int(f"pos_{articles[i]}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7 and all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# No consecutive same-topic constraint
# For each adjacent position pair (k, k+1), enforce that articles at those positions have different topics
for k in range(1, 7):
    # For each pair of articles (i, j), if article i is at position k and article j is at position k+1,
    # then topics[i] != topics[j]
    for i in range(7):
        for j in range(7):
            if topics[i] == topics[j]:
                solver.add(Not(And(pos[i] == k, pos[j] == k + 1)))

# S can be earlier than Q only if Q is third: (pos_S < pos_Q) → (pos_Q == 3)
# Equivalent to: pos_Q != 3 → pos_S > pos_Q
solver.add(Implies(pos[5] != 3, pos[5] < pos[3]))

# S must be earlier than Y: pos_S < pos_Y
solver.add(pos[5] < pos[6])

# J must be earlier than G, and G must be earlier than R: pos_J < pos_G < pos_R
solver.add(pos[2] < pos[0], pos[0] < pos[4])

# Answer choices
answer_choices = [
    ("H is fourth.", lambda: pos[1] == 4),
    ("H is sixth.", lambda: pos[1] == 6),
    ("R is fourth.", lambda: pos[4] == 4),
    ("R is seventh.", lambda: pos[4] == 7),
    ("Y is fifth.", lambda: pos[6] == 5)
]

# Check each answer choice for uniqueness
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the condition
    s_chk.add(condition())
    
    if s_chk.check() == unsat:
        # No solution exists under this condition, skip
        continue
    
    # Get first model
    m1 = s_chk.model()
    
    # Create constraint to exclude this exact assignment
    forbid_m1 = []
    for i in range(7):
        val = m1.eval(pos[i])
        forbid_m1.append(pos[i] != val)
    s_chk.add(Or(*forbid_m1))
    
    # Check if a second model exists
    if s_chk.check() == unsat:
        # Only one solution exists, so this condition fully determines the order
        answer_index_list.append(idx)

print(answer_index_list)