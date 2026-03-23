from z3 import *

# Articles and their topics
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic = {"G": 0, "H": 0, "J": 0, "Q": 1, "R": 1, "S": 1, "Y": 2}  # 0: finance, 1: nutrition, 2: wildlife

# Position variables
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# No consecutive same topic constraint
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of articles a and b, if |pos[a] - pos[b]| == 1 then topics must differ
        # Instead of absolute difference, we'll check all adjacent position pairs explicitly
        pass

# Better approach: for each pair of articles, if they have same topic, they cannot be adjacent
for a1 in articles:
    for a2 in articles:
        if a1 != a2 and topic[a1] == topic[a2]:
            solver.add(Abs(pos[a1] - pos[a2]) != 1)

# S before Q conditional: (S < Q) => (Q == 3)
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S before Y
solver.add(pos["S"] < pos["Y"])

# J before G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    ("H is fourth.", lambda: pos["H"] == 4),
    ("H is sixth.", lambda: pos["H"] == 6),
    ("R is fourth.", lambda: pos["R"] == 4),
    ("R is seventh.", lambda: pos["R"] == 7),
    ("Y is fifth.", lambda: pos["Y"] == 5)
]

# Check each answer choice for uniqueness
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific constraint from answer choice
    constraint()
    
    if s_chk.check() == sat:
        # Get one model
        m = s_chk.model()
        
        # Build the exact assignment as a constraint to exclude
        exact_assignment = And([pos[a] == m.eval(pos[a]).as_long() for a in articles])
        
        # Check if there's another distinct solution
        s_unique = Solver()
        s_unique.add(solver.assertions())
        constraint()
        s_unique.add(Not(exact_assignment))
        
        if s_unique.check() == unsat:
            # Only one solution exists
            answer_index_list.append(idx)

print(answer_index_list)