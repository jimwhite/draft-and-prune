from z3 import *

# Scientists: botanists [F, G, H], chemists [K, L, M], zoologists [P, Q, R]
F, G, H = Bools("F G H")
K, L, M = Bools("K L M")
P, Q, R = Bools("P Q R")

# Base solver with all constraints
solver = Solver()

# Panel size constraint: exactly 5 scientists
solver.add(Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0),
                If(K, 1, 0), If(L, 1, 0), If(M, 1, 0),
                If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)]) == 5)

# Representation constraint: at least one from each discipline
solver.add(Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)]) >= 1)
solver.add(Sum([If(K, 1, 0), If(L, 1, 0), If(M, 1, 0)]) >= 1)
solver.add(Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)]) >= 1)

# Conditional constraint: if more than one botanist, then at most one zoologist
botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(botanists >= 2, zoologists <= 1))

# Exclusion constraint: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Exclusion constraint: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Conditional constraint: if M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Answer choices
answer_choices = [
    {"F": True, "G": True, "K": True, "P": True, "Q": True},
    {"G": True, "H": True, "K": True, "L": True, "M": True},
    {"G": True, "H": True, "K": True, "L": True, "R": True},
    {"H": True, "K": True, "M": True, "P": True, "R": True},
    {"H": True, "L": True, "M": True, "P": True, "Q": True}
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the exact selection pattern
    for scientist, selected in choice.items():
        if scientist == "F":
            s_chk.add(F == selected)
        elif scientist == "G":
            s_chk.add(G == selected)
        elif scientist == "H":
            s_chk.add(H == selected)
        elif scientist == "K":
            s_chk.add(K == selected)
        elif scientist == "L":
            s_chk.add(L == selected)
        elif scientist == "M":
            s_chk.add(M == selected)
        elif scientist == "P":
            s_chk.add(P == selected)
        elif scientist == "Q":
            s_chk.add(Q == selected)
        elif scientist == "R":
            s_chk.add(R == selected)
    
    # Ensure unmentioned scientists are not selected
    for scientist in ["F", "G", "H", "K", "L", "M", "P", "Q", "R"]:
        if scientist not in choice:
            if scientist == "F":
                s_chk.add(F == False)
            elif scientist == "G":
                s_chk.add(G == False)
            elif scientist == "H":
                s_chk.add(H == False)
            elif scientist == "K":
                s_chk.add(K == False)
            elif scientist == "L":
                s_chk.add(L == False)
            elif scientist == "M":
                s_chk.add(M == False)
            elif scientist == "P":
                s_chk.add(P == False)
            elif scientist == "Q":
                s_chk.add(Q == False)
            elif scientist == "R":
                s_chk.add(R == False)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)