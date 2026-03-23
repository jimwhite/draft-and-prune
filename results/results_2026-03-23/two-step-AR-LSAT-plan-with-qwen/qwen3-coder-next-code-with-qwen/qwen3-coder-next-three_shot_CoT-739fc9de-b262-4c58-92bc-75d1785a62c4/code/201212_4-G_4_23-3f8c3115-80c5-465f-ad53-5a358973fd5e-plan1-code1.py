from z3 import *

# Articles and their topics
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic = {
    "G": 0, "H": 0, "J": 0,  # finance
    "Q": 1, "R": 1, "S": 1,  # nutrition
    "Y": 2                   # wildlife
}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions are distinct integers from 1 to 7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic-consecutive constraint: no two consecutive positions have same topic
for i in range(1, 7):
    for a1 in articles:
        for a2 in articles:
            if topic[a1] == topic[a2]:
                solver.add(Not(And(pos[a1] == i, pos[a2] == i + 1)))
                solver.add(Not(And(pos[a2] == i, pos[a1] == i + 1)))

# S-Q conditional: if S is earlier than Q, then Q must be third
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S-Y constraint: S must be earlier than Y
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
unique_answer = None
for desc, constraint_fn in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the constraint directly
    if desc == "H is fourth.":
        s_chk.add(pos["H"] == 4)
    elif desc == "H is sixth.":
        s_chk.add(pos["H"] == 6)
    elif desc == "R is fourth.":
        s_chk.add(pos["R"] == 4)
    elif desc == "R is seventh.":
        s_chk.add(pos["R"] == 7)
    elif desc == "Y is fifth.":
        s_chk.add(pos["Y"] == 5)
    
    if s_chk.check() == sat:
        # Get one model
        m = s_chk.model()
        
        # Build assignment from model
        assignment = {}
        for a in articles:
            val = m.eval(pos[a])
            if is_int_value(val):
                assignment[a] = val.as_long()
        
        # Check uniqueness: add constraint that at least one position differs
        s_unique = Solver()
        s_unique.add(solver.assertions())
        
        # Add the same assumption
        if desc == "H is fourth.":
            s_unique.add(pos["H"] == 4)
        elif desc == "H is sixth.":
            s_unique.add(pos["H"] == 6)
        elif desc == "R is fourth.":
            s_unique.add(pos["R"] == 4)
        elif desc == "R is seventh.":
            s_unique.add(pos["R"] == 7)
        elif desc == "Y is fifth.":
            s_unique.add(pos["Y"] == 5)
        
        # Add constraint that at least one article differs from the found assignment
        diff_constraint = Or(*[pos[a] != assignment[a] for a in articles])
        s_unique.add(diff_constraint)
        
        if s_unique.check() == unsat:
            unique_answer = desc
            break

print(unique_answer)