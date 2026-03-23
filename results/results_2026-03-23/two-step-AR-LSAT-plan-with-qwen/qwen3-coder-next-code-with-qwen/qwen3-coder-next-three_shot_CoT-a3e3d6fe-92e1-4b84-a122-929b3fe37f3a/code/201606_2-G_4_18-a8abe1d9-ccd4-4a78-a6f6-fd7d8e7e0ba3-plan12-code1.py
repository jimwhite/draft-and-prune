from z3 import *

# Singer indices: 0=Kammer, 1=Lugo, 2=Trillo, 3=Waite, 4=Yoshida, 5=Zinn
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
singer_idx = {name: i for i, name in enumerate(singers)}

# Answer choices as lists of singer names in order
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Create position variables
pos = {name: Int(f"pos_{name}") for name in singers}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for name in singers:
    solver.add(pos[name] >= 1, pos[name] <= 6)
solver.add(Distinct(*[pos[name] for name in singers]))

# Recording constraints:
# - Kammer and Lugo are the only recorded auditions
# - Position 4 cannot be recorded → Kammer and Lugo ≠ position 4
solver.add(pos["Kammer"] != 4)
solver.add(pos["Lugo"] != 4)
# - Position 5 must be recorded → at least one of Kammer or Lugo is at position 5
solver.add(Or(pos["Kammer"] == 5, pos["Lugo"] == 5))

# Waite constraint: earlier than both recorded auditions
solver.add(pos["Waite"] < pos["Kammer"])
solver.add(pos["Waite"] < pos["Lugo"])

# Kammer before Trillo
solver.add(pos["Kammer"] < pos["Trillo"])

# Zinn before Yoshida
solver.add(pos["Zinn"] < pos["Yoshida"])

# Check each answer choice by evaluating the permutation
valid_indices = []
for idx, order in enumerate(answer_choices):
    # Create a new solver for this specific order
    s = Solver()
    s.add(solver.assertions())
    
    # Add constraints that match the order
    for i, name in enumerate(order):
        s.add(pos[name] == i + 1)
    
    if s.check() == sat:
        valid_indices.append(idx)

# Print the indices of valid orders
print(valid_indices)