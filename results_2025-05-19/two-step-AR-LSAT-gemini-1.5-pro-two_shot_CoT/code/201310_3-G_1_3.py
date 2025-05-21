from z3 import *

# Define bands and slots
U, V, W, X, Y, Z = 0, 1, 2, 3, 4, 5
band_at_slot = Array('band_at_slot', IntSort(), IntSort())
i = Int('i')

# Create solver and add constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([band_at_slot[i] for i in range(1, 7)]))

# Define IndexOf
def IndexOf(B):
    return Sum([If(band_at_slot[i] == B, i, 0) for i in range(1, 7)])

# Constraint 2 (V before Z)
solver.add(IndexOf(V) < IndexOf(Z))

# Constraint 3 (W before X)
solver.add(IndexOf(W) < IndexOf(X))

# Constraint 4 (Z before X)
solver.add(IndexOf(Z) < IndexOf(X))

# Constraint 5 (U in last three)
solver.add(Or(band_at_slot[4] == U, band_at_slot[5] == U, band_at_slot[6] == U))

# Constraint 6 (Y in first three)
solver.add(Or(band_at_slot[1] == Y, band_at_slot[2] == Y, band_at_slot[3] == Y))

# Constraint 7 (V in slot 3)
solver.add(band_at_slot[3] == V)

# Check answer choices
answer_choices = [
    IndexOf(X) < IndexOf(U),  # A
    IndexOf(Z) < IndexOf(W),  # B
    IndexOf(U) < IndexOf(X),  # C
    IndexOf(W) < IndexOf(Y),  # D
    IndexOf(U) < IndexOf(Z)   # E
]

for option_index, negation in enumerate(answer_choices):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()