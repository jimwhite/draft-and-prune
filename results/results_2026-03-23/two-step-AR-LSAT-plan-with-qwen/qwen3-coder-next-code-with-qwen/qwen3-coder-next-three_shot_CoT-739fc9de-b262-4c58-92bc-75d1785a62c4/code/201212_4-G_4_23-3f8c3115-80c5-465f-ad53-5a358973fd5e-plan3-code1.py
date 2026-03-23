from z3 import *

# Article indices: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic_map = [0, 0, 0, 1, 1, 1, 2]  # Finance: G,H,J (0); Nutrition: Q,R,S (1); Wildlife: Y (2)

# Position variables
pos = [Int(f"pos_{articles[i]}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(pos))

# Topic constraints: no consecutive same topics
for i in range(7):
    for j in range(i + 1, 7):
        solver.add(Implies(Abs(pos[i] - pos[j]) == 1, topic_map[i] != topic_map[j]))

# Relative ordering constraints
solver.add(pos[5] < pos[6])  # S before Y (S=5, Y=6)
solver.add(pos[2] < pos[0])  # J before G (J=2, G=0)
solver.add(pos[0] < pos[4])  # G before R (G=0, R=4)

# S can be earlier than Q only if Q is third: (S < Q) → (Q == 3)
# Equivalent to: (Q >= S) OR (Q == 3)
solver.add(Or(pos[3] == 3, pos[5] >= pos[3]))

# Answer choices: indices correspond to options
answer_choices = [
    ("H is fourth.", 1, 4),   # H=1, position=4
    ("H is sixth.", 1, 6),    # H=1, position=6
    ("R is fourth.", 4, 4),   # R=4, position=4
    ("R is seventh.", 4, 7),  # R=4, position=7
    ("Y is fifth.", 6, 5)     # Y=6, position=5
]

# Check each answer choice for uniqueness
answer_index_list = []
for idx, (desc, art_idx, pos_val) in enumerate(answer_choices):
    s = Solver()
    s.add(solver.assertions())
    
    # Add the candidate constraint
    s.add(pos[art_idx] == pos_val)
    
    if s.check() == sat:
        m = s.model()
        # Get the model values for all positions
        model_vals = [m.evaluate(pos[i]).as_long() for i in range(7)]
        
        # Check uniqueness: add constraint that at least one position differs
        s_unique = Solver()
        s_unique.add(solver.assertions())
        s_unique.add(pos[art_idx] == pos_val)
        
        # Add constraint that at least one position differs from current model
        diff_constraint = Or(*[pos[i] != model_vals[i] for i in range(7)])
        s_unique.add(diff_constraint)
        
        if s_unique.check() == unsat:
            # Unique solution found
            answer_index_list.append(idx)
    else:
        # Not even satisfiable, so cannot determine order
        pass

# Print the index of the answer choice that makes the order fully determined
print(answer_index_list)