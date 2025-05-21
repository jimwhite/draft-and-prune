from z3 import *

# Define constants for musicians
G = 0
K = 1
P = 2
S = 3
T = 4
V = 5

# Define the solo order array
solo_order = Array('solo_order', IntSort(), IntSort())

# Create a solver instance
solver = Solver()

# Helper function to get the solo slot of a musician
def get_solo_slot(musician):
    for i in range(1, 7):
        if solver.check(solo_order[i] == musician) == sat:
            return i
    return -1  # Should not happen if constraints are correct


# Constraint 1: Domain
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(solo_order[i] >= 0, solo_order[i] <= 5))))

# Constraint 2: Distinctness
solver.add(Distinct([solo_order[i] for i in range(1, 7)]))

# Constraint 3: Guitarist not 4th
solver.add(solo_order[4] != G)

# Constraint 4: Percussionist before Keyboard
solver.add(get_solo_slot(P) < get_solo_slot(K))


# Constraint 5: Violinist before Keyboard before Guitarist
solver.add(get_solo_slot(V) < get_solo_slot(K))
solver.add(get_solo_slot(K) < get_solo_slot(G))

# Constraint 6: Saxophonist after P or T, not both
solver.add(Xor(get_solo_slot(P) < get_solo_slot(S), get_solo_slot(T) < get_solo_slot(S)))

# Add constraint: Violinist performs 4th
solver.add(solo_order[4] == V)

# Check answer choices
answer_choices = [
    Not(get_solo_slot(P) < get_solo_slot(V)),
    Not(get_solo_slot(T) < get_solo_slot(V)),
    Not(get_solo_slot(T) < get_solo_slot(G)),
    Not(get_solo_slot(S) < get_solo_slot(V)),
    Not(get_solo_slot(T) < get_solo_slot(S))
]

for idx, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()