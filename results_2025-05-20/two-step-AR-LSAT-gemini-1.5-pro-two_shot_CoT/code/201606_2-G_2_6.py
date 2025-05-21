from z3 import *

# Define variables
year_assignment = Array('year_assignment', IntSort(), IntSort())
i = Int('i')

# Create solver and add general constraints
solver = Solver()
solver.add(ForAll(i, Implies(And(i >= 0, i < 4), And(year_assignment[i] >= 0, year_assignment[i] < 6))))
solver.add(Distinct([year_assignment[j] for j in range(4)]))
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4))
solver.add(Implies(Or([year_assignment[j] == 1 for j in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1)))
solver.add(Implies(Or([year_assignment[j] == 4 for j in range(4)]), Or([year_assignment[j] == 3 for j in range(4)])))
solver.add(Implies(Or([year_assignment[j] == 3 for j in range(4)]), Or(And(year_assignment[0] == 2, year_assignment[1] == 3), And(year_assignment[1] == 2, year_assignment[2] == 3), And(year_assignment[2] == 2, year_assignment[3] == 3))))


# Answer choices
choices = [
    ["Louis", "Onyx", "Ryan", "Yoshio"],
    ["Mollie", "Yoshio", "Tiffany", "Onyx"],
    ["Onyx", "Ryan", "Louis", "Tiffany"],
    ["Tiffany", "Onyx", "Louis", "Ryan"],
    ["Yoshio", "Onyx", "Louis", "Mollie"]
]
student_mapping = {"Louis": 0, "Mollie": 1, "Onyx": 2, "Ryan": 3, "Tiffany": 4, "Yoshio": 5}

# Check each answer choice
for option_index, choice in enumerate(choices):
    solver.push()
    for year_index, student_name in enumerate(choice):
        solver.add(year_assignment[year_index] == student_mapping[student_name])
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()