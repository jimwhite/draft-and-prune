from z3 import *

# Article indices: G, H, J, Q, R, S, Y
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
# Topic mapping: 0=finance, 1=nutrition, 2=wildlife
topic_map = {
    "G": 0, "H": 1, "J": 0,
    "Q": 1, "R": 1, "S": 1,
    "Y": 2
}

# Position variables: pos[i] = position of article i (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic-consecutive constraint: no two consecutive same topics
for i in range(1, 7):
    # For each position i (1-indexed), find articles at positions i and i+1
    # We need to express: if article X is at position i, article Y at i+1, then topic(X) != topic(Y)
    # Instead, use: for all pairs of articles a,b with same topic, they cannot be consecutive
    for j in range(len(articles)):
        for k in range(j + 1, len(articles)):
            a1 = articles[j]
            a2 = articles[k]
            if topic_map[a1] == topic_map[a2]:
                solver.add(Not(And(pos[a1] == i, pos[a2] == i + 1)))
                solver.add(Not(And(pos[a1] == i + 1, pos[a2] == i)))

# S-before-Q conditional: S < Q → Q == 3
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S-before-Y constraint
solver.add(pos["S"] < pos["Y"])

# J-G-R chain: J < G < R
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

answer_index_list = []

for idx, (desc, constraint) in enumerate(answer_choices):
    # Clone solver
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific constraint
    s_chk.add(constraint())
    
    # Check for uniqueness: find first model, block it, check again
    if s_chk.check() == sat:
        m = s_chk.model()
        
        # Build constraint to block this model
        block = []
        for a in articles:
            val = m.eval(pos[a])
            if is_int_value(val):
                block.append(pos[a] != val.as_long())
            else:
                # Shouldn't happen for integer positions, but just in case
                block.append(pos[a] != val)
        
        # Add blocking constraint and check again
        s_chk2 = Solver()
        s_chk2.add(solver.assertions())
        s_chk2.add(constraint())
        s_chk2.add(Or(*block))
        
        if s_chk2.check() == unsat:
            # Only one model exists
            answer_index_list.append(idx)
    else:
        # No solution, so not fully determined (we need exactly one solution)
        pass

print(answer_index_list)