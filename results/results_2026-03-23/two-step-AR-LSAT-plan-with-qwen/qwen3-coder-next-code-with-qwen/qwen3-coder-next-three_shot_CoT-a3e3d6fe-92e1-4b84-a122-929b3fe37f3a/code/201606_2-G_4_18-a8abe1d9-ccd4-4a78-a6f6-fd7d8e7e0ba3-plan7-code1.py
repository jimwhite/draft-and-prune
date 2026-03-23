from z3 import *

# Singers and their recorded status
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
recorded = {"Kammer", "Lugo"}

# Create position variables
pos = {s: Int(f"pos_{s}") for s in singers}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)
solver.add(Distinct(*[pos[s] for s in singers]))

# Recorded position constraints
# Position 4 cannot be recorded (not Kammer or Lugo)
solver.add(And(pos["Kammer"] != 4, pos["Lugo"] != 4))
# Position 5 must be recorded (Kammer or Lugo)
solver.add(Or(pos["Kammer"] == 5, pos["Lugo"] == 5))

# Ordering constraints
# Waite's audition must take place earlier than the two recorded auditions (Kammer and Lugo)
solver.add(pos["Waite"] < pos["Kammer"])
solver.add(pos["Waite"] < pos["Lugo"])

# Kammer's audition must take place earlier than Trillo's audition
solver.add(pos["Kammer"] < pos["Trillo"])

# Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos["Zinn"] < pos["Yoshida"])

# Answer choices (orderings)
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each choice
valid_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix positions according to the choice
    for i, singer in enumerate(choice):
        s_chk.add(pos[singer] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)