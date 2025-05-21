from z3 import *

# Define variables
I_W, I_V, S_W, S_V, T_W, T_V = Ints('I_W I_V S_W S_V T_W T_V')

# Create solver
solver = Solver()

# Add constraints
solver.add(And(I_W >= 1, I_W <= 3))
solver.add(And(I_V >= 1, I_V <= 3))
solver.add(And(S_W >= 1, S_W <= 3))
solver.add(And(S_V >= 1, S_V <= 3))
solver.add(And(T_W >= 1, T_W <= 3))
solver.add(And(T_V >= 1, T_V <= 3))

solver.add(I_W <= I_V)
solver.add(S_W <= S_V)
solver.add(T_W <= T_V)

solver.add(I_V < S_V)
solver.add(I_V < T_V)

solver.add(S_W < T_W)

solver.add(I_W != 2)
solver.add(S_W != 2)
solver.add(T_W != 2)

# Check answer choices
options = [
    I_W < S_W,  # A
    S_W < I_W,  # B
    S_V < T_V,  # C
    T_W < I_W,  # D
    T_V < S_V   # E
]

option_letters = ['A', 'B', 'C', 'D', 'E']

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {option_letters[i]} is correct")
        exit()
    solver.pop()