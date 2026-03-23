from z3 import *

# Singer indices: 0=Kammer, 1=Lugo, 2=Trillo, 3=Waite, 4=Yoshida, 5=Zinn
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
K, L, T, W, Y, Z = range(6)

# Position variables: pos[singer] = position (1-6)
pos = {s: Int(f"pos_{s}") for s in singers}

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct (1-6)
solver.add(Distinct(*pos.values()))
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# Recording constraints
# Kammer and Lugo are recorded; others (Trillo, Waite, Yoshida, Zinn) are not
# Fourth audition cannot be recorded → position 4 must be assigned to non-recorded singer
solver.add(Or(pos["Trillo"] == 4, pos["Waite"] == 4, pos["Yoshida"] == 4, pos["Zinn"] == 4))
# Fifth audition must be recorded → position 5 must be assigned to Kammer or Lugo
solver.add(Or(pos["Kammer"] == 5, pos["Lugo"] == 5))

# Waite constraint: Waite before both recorded auditions (Kammer and Lugo)
solver.add(pos["Waite"] < pos["Kammer"])
solver.add(pos["Waite"] < pos["Lugo"])

# Kammer before Trillo
solver.add(pos["Kammer"] < pos["Trillo"])

# Zinn before Yoshida
solver.add(pos["Zinn"] < pos["Yoshida"])

# Answer choices (as lists of singer names in order)
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each answer choice
satisfiable_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the exact order: position i+1 for choice[i]
    for i, singer in enumerate(choice):
        s_chk.add(pos[singer] == i + 1)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

# Print the indices of satisfiable choices (should be exactly one)
print(satisfiable_indices)