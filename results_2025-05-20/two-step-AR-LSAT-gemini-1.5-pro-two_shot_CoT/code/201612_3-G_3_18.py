from z3 import *

# 1. Entities
F = 0
G = 1
H = 2
I = 3
O = 0
W = 1
W1 = 0
W2 = 1
W3 = 2
W4 = 3
U = 0
L = 1
FO = 0
FW = 1
GO = 2
GW = 3
HO = 4
HW = 5
IO = 6
IW = 7
W1U = 0
W1L = 1
W2U = 2
W2L = 3
W3U = 4
W3L = 5
W4U = 6
W4L = 7

# 2. Variables
painting_at = Array('painting_at', IntSort(), IntSort())

# 3. Constraints Helper Functions/Arrays
student_of = [F, F, G, G, H, H, I, I]
type_of = [O, W, O, W, O, W, O, W]

# Solver
solver = Solver()

# Constraint 1: All paintings placed exactly once
solver.add(Distinct([painting_at[i] for i in range(8)]))

# Constraint 2: No wall has only watercolors
for w in range(4):
    solver.add(Or(type_of[painting_at[w*2+U]] == O, type_of[painting_at[w*2+L]] == O))

# Constraint 3: No wall has work of only one student
for w in range(4):
    solver.add(student_of[painting_at[w*2+U]] != student_of[painting_at[w*2+L]])

# Constraint 4: No Franz and Isaacs on same wall
for w in range(4):
    solver.add(Not(And(student_of[painting_at[w*2+U]] == F, student_of[painting_at[w*2+L]] == I)))
    solver.add(Not(And(student_of[painting_at[w*2+U]] == I, student_of[painting_at[w*2+L]] == F)))

# Constraint 5: Greene's watercolor upper, Franz's oil lower, same wall
solver.add(Or([And(painting_at[w*2+U] == GW, painting_at[w*2+L] == FO) for w in range(4)]))

# Constraint 6: Isaacs's oil on wall 4 lower
solver.add(painting_at[W4*2+L] == IO)


# 4. Answering the Question
options = [
    "Franz's watercolor is displayed on the same wall as Greene's oil.",
    "Franz's watercolor is displayed on the same wall as Hidalgo's oil.",
    "Greene's oil is displayed in an upper position.",
    "Hidalgo's watercolor is displayed in a lower position.",
    "Isaacs's watercolor is displayed on the same wall as Hidalgo's oil."
]

for i, option in enumerate(options):
    solver.push()
    if i == 0:  # Option A
        solver.add(Or([And(painting_at[j] == FW, painting_at[k] == GO, j // 2 == k // 2) for j in range(8) for k in range(8)]))
    elif i == 1:  # Option B
        solver.add(Or([And(painting_at[j] == FW, painting_at[k] == HO, j // 2 == k // 2) for j in range(8) for k in range(8)]))
    elif i == 2:  # Option C
        solver.add(Or([And(painting_at[j] == GO, j % 2 == U) for j in range(8)]))
    elif i == 3:  # Option D
        solver.add(Or([And(painting_at[j] == HW, j % 2 == L) for j in range(8)]))
    elif i == 4:  # Option E
        solver.add(Or([And(painting_at[j] == IW, painting_at[k] == HO, j // 2 == k // 2) for j in range(8) for k in range(8)]))

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

