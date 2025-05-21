from z3 import *

# Variables
assigned = Array('assigned', IntSort(), BoolSort())
university = Array('university', IntSort(), IntSort())
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(0 <= i, i < 6), assigned[i] == Or(university[i] == 0, university[i] == 1))))
solver.add(Sum([If(And(assigned[i], university[i] == 0), 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(And(assigned[i], university[i] == 1), 1, 0) for i in range(6)]) >= 2)
solver.add(assigned[0] == True)
solver.add(assigned[2] == True)
solver.add(university[0] == university[2])
solver.add(Implies(And(assigned[4], assigned[5]), university[4] != university[5]))
solver.add(Implies(And(assigned[1], university[1] == 0), And(assigned[4], university[4] == 1)))
solver.add(Implies(Not(And(assigned[3], university[3] == 1)), And(assigned[2], university[2] == 1, assigned[5], university[5] == 1)))

# Check which photographers must be assigned
must_be_assigned_photographers = []
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
for i in range(6):
    solver.push()
    solver.add(Not(assigned[i]))
    if solver.check() == unsat:
        must_be_assigned_photographers.append(photographers[i])
    solver.pop()

# Check answer choices
answers = [
    ["Frost", "Heideck"],
    ["Frost", "Heideck", "Knutson"],
    ["Frost", "Heideck", "Knutson", "Lai"],
    ["Frost", "Gonzalez", "Heideck"],
    ["Frost", "Gonzalez", "Heideck", "Mays"]
]

for idx, answer in enumerate(answers):
    if set(answer) == set(must_be_assigned_photographers):
        print(f"Option {chr(65 + idx)} is correct")
        exit()