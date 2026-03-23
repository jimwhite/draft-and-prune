from z3 import *

# Singers
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = {s: Int(f"pos_{s}") for s in singers}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)
solver.add(Distinct(*[pos[s] for s in singers]))

# Recorded singers: Kammer, Lugo
recorded = {"Kammer", "Lugo"}

# Fourth audition is unrecorded: the singer at position 4 must not be Kammer or Lugo
# We'll encode this as: for any singer s, if pos[s] == 4 then s not in recorded
# But easier: add constraints that Kammer and Lugo are NOT at position 4
solver.add(pos["Kammer"] != 4)
solver.add(pos["Lugo"] != 4)

# Fifth audition must be recorded: singer at position 5 must be Kammer or Lugo
solver.add(Or(pos["Kammer"] == 5, pos["Lugo"] == 5))

# Waite's audition must take place earlier than the two recorded auditions
solver.add(pos["Waite"] < pos["Kammer"])
solver.add(pos["Waite"] < pos["Lugo"])

# Kammer's audition must take place earlier than Trillo's audition
solver.add(pos["Kammer"] < pos["Trillo"])

# Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos["Zinn"] < pos["Yoshida"])

# Answer choices (each is a list of singers in order from first to sixth)
choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each choice
satisfiable_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exact positions: first singer at position 1, second at 2, etc.
    for i, s in enumerate(choice):
        s_chk.add(pos[s] == i + 1)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

# Output the index of the satisfiable choice (0-based)
print(satisfiable_indices[0] if satisfiable_indices else -1)