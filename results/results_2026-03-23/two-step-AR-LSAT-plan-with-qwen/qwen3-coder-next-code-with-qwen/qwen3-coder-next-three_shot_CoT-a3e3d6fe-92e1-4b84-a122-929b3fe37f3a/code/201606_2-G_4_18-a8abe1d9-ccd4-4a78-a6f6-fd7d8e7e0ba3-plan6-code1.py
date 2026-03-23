from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
indices = {s: i for i, s in enumerate(singers)}

# Candidate orders (as lists of singer names)
candidate_orders = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Base solver with constraints
def create_base_solver():
    solver = Solver()
    
    # Position variables: pos[i] is the position (1-6) of singer i
    pos = [Int(f"pos_{i}") for i in range(6)]
    
    # Domain: positions 1-6
    for i in range(6):
        solver.add(pos[i] >= 1, pos[i] <= 6)
    
    # All positions distinct
    solver.add(Distinct(pos))
    
    # Recording constraints:
    # Kammer (0) and Lugo (1) are recorded; others not
    # Fourth audition cannot be recorded => position 4 must be one of Trillo(2), Waite(3), Yoshida(4), Zinn(5)
    # Fifth audition must be recorded => position 5 must be Kammer(0) or Lugo(1)
    
    # Create inverse mapping: inv[p] = singer index at position p (p=1..6)
    inv = [Int(f"inv_{p}") for p in range(7)]  # indices 0-6, use 1..6
    
    # Link pos and inv using ForAll constraints
    for i in range(6):
        for p in range(1, 7):
            solver.add(Implies(pos[i] == p, inv[p] == i))
    
    # Position 4 (4th audition) must not be Kammer or Lugo
    solver.add(inv[4] != 0, inv[4] != 1)
    
    # Position 5 (5th audition) must be Kammer or Lugo
    solver.add(Or(inv[5] == 0, inv[5] == 1))
    
    # Waite (3) must be before both recorded auditions (Kammer=0, Lugo=1)
    solver.add(pos[3] < pos[0])
    solver.add(pos[3] < pos[1])
    
    # Kammer (0) before Trillo (2)
    solver.add(pos[0] < pos[2])
    
    # Zinn (5) before Yoshida (4)
    solver.add(pos[5] < pos[4])
    
    return solver, pos

# Check each candidate order
valid_indices = []
for idx, order in enumerate(candidate_orders):
    solver, pos = create_base_solver()
    
    # Constrain positions to match the candidate order
    for rank, singer in enumerate(order):
        singer_idx = indices[singer]
        solver.add(pos[singer_idx] == rank + 1)
    
    if solver.check() == sat:
        valid_indices.append(idx)

# Print the index of the valid choice (should be exactly one)
print(valid_indices[0] if valid_indices else -1)