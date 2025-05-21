from z3 import *

# Accomplices and positions
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
positions = range(7)

# Recruitment order variable (array mapping position to accomplice index)
recruitment = Array('recruitment', IntSort(), IntSort())

solver = Solver()

# Constraints: Each accomplice assigned to exactly one position, and vice-versa
solver.add(Distinct([recruitment[i] for i in positions]))
for i in positions:
    solver.add(And(recruitment[i] >= 0, recruitment[i] < len(accomplices)))

# Stanton not before or after Tao
for i in positions:
    if i > 0:
        solver.add(Implies(recruitment[i] == accomplices.index("Stanton"), recruitment[i-1] != accomplices.index("Tao")))
    if i < 6:
        solver.add(Implies(recruitment[i] == accomplices.index("Stanton"), recruitment[i+1] != accomplices.index("Tao")))

# Quinn earlier than Rovero
solver.add(Sum([If(recruitment[i] == accomplices.index("Quinn"), 1, 0) * i for i in positions]) < Sum([If(recruitment[i] == accomplices.index("Rovero"), 1, 0) * i for i in positions]))

# Villas immediately before White
for i in range(6):
    solver.add(Implies(recruitment[i] == accomplices.index("Villas"), recruitment[i+1] == accomplices.index("White")))

# Peters recruited fourth
solver.add(recruitment[3] == accomplices.index("Peters"))

# Premise: Quinn immediately before Rovero
for i in range(6):
    solver.add(Implies(recruitment[i] == accomplices.index("Quinn"), recruitment[i+1] == accomplices.index("Rovero")))

# Check answer choices
answer_positions = [0, 1, 2, 4, 6]  # first, second, third, fifth, seventh
answer_options = ["A", "B", "C", "D", "E"]

for option_index, pos in enumerate(answer_positions):
    solver.push()
    solver.add(recruitment[pos] == accomplices.index("Stanton"))
    if solver.check() == unsat:
        print(f"Option {answer_options[option_index]} is correct")
        exit()
    solver.pop()