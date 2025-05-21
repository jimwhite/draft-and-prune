from z3 import *

# 1. Define entities
RealProp, Southco, Trustcorp = 0, 1, 2
Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = 0, 1, 2, 3, 4, 5, 6, 7
Class1, Class2, Class3 = 0, 1, 2

# 2. Define initial state
initial_owner = Array('initial_owner', IntSort(), IntSort())
building_class = Array('building_class', IntSort(), IntSort())

initial_ownership = {
    Garza: RealProp, Yates: RealProp, Zimmer: RealProp,
    Flores: Southco, Lynch: Southco,
    King: Trustcorp, Meyer: Trustcorp, Ortiz: Trustcorp
}
building_classes = {
    Garza: Class1, Flores: Class1,
    Lynch: Class2, King: Class2, Meyer: Class2, Ortiz: Class2,
    Yates: Class3, Zimmer: Class3
}

# 5. Constraint: Valid company IDs (Solver defined here)
solver = Solver()

for b in range(8):
    solver.add(initial_owner[b] == initial_ownership[b])
    solver.add(building_class[b] == building_classes[b])

# 3. Calculate initial counts
N_initial = [[0] * 3 for _ in range(3)]
for c in range(3):
    for k in range(3):
        N_initial[c][k] = Sum([If(And(initial_owner[b] == c, building_class[b] == k), 1, 0) for b in range(8)])

# 4. Define final state
owns = Array('owns', IntSort(), IntSort())

for b in range(8):
    solver.add(And(owns[b] >= 0, owns[b] <= 2))

# 6. Define final counts
N_final = [[0] * 3 for _ in range(3)]
for c in range(3):
    for k in range(3):
        N_final[c][k] = Sum([If(And(owns[b] == c, building_class[b] == k), 1, 0) for b in range(8)])

# 7. Constraint: Trade rules (simplified for RealProp and Class 2)
for b in range(8):
    solver.add(Implies(
        And(building_class[b] == Class2, initial_owner[b] != RealProp, owns[b] == RealProp),
        And(N_final[RealProp][Class3] <= N_initial[RealProp][Class3] - 2,
            Or([N_final[c][Class3] >= N_initial[c][Class3] + 2 for c in range(3)]))
    ))

# 9. Check answer choices
options = [
    {Lynch: RealProp, Meyer: RealProp, Ortiz: RealProp},  # A
    {Garza: Southco, Meyer: Southco},  # B
    {King: Southco, Meyer: Southco, Ortiz: Southco},  # C
    {Flores: Trustcorp, Yates: Trustcorp},  # D
    {Garza: Trustcorp, Lynch: Trustcorp}  # E
]

for i, option in enumerate(options):
    solver.push()
    for building, company in option.items():
        solver.add(owns[building] == company)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
