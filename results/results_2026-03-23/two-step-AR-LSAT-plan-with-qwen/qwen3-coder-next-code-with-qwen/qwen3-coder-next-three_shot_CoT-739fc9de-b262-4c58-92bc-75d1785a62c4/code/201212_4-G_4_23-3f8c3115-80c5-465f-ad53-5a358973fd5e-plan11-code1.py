from z3 import *

# Articles and their topics
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
finance = {"G", "H", "J"}
nutrition = {"Q", "R", "S"}
wildlife = {"Y"}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic-consecutive constraint: no two consecutive positions have same topic
for k in range(1, 7):
    for a in articles:
        for b in articles:
            if a != b and ((a in finance and b in finance) or 
                           (a in nutrition and b in nutrition) or
                           (a in wildlife and b in wildlife)):
                solver.add(Not(And(pos[a] == k, pos[b] == k + 1)))

# S-Q conditional constraint: if S < Q then Q must be third
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S-Y constraint: S before Y
solver.add(pos["S"] < pos["Y"])

# J-G-R chain: J before G, G before R
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
    # Clone base solver
    s = Solver()
    s.add(solver.assertions())
    
    # Add the constraint for this answer choice
    constraint()
    s.add(constraint.__globals__.get('pos_H') == 4 if idx == 0 else 
          pos["H"] == 6 if idx == 1 else
          pos["R"] == 4 if idx == 2 else
          pos["R"] == 7 if idx == 3 else
          pos["Y"] == 5)
    
    # Check satisfiability
    if s.check() == sat:
        m = s.model()
        
        # Create a model representation for comparison
        model_vals = {a: m.evaluate(pos[a]).as_long() for a in articles}
        
        # Add constraint to find another different solution
        s2 = Solver()
        s2.add(solver.assertions())
        constraint()
        s2.add(constraint.__globals__.get('pos_H') == 4 if idx == 0 else 
               pos["H"] == 6 if idx == 1 else
               pos["R"] == 4 if idx == 2 else
               pos["R"] == 7 if idx == 3 else
               pos["Y"] == 5)
        # Add constraint that at least one position differs from the first model
        s2.add(Or(*[pos[a] != model_vals[a] for a in articles]))
        
        if s2.check() == unsat:
            # Unique solution found
            answer_index_list.append(idx)

print(answer_index_list)