from z3 import *

# Define employees and parking spaces
employees = {"R": 0, "S": 1, "T": 2, "V": 3, "X": 4, "Y": 5}
parking_spaces = list(range(1, 7))

# Create a Z3 function representing the assignment
f = Function("f", IntSort(), IntSort())

# Create a solver
solver = Solver()

# Add constraints for distinct parking spaces
solver.add(Distinct([f(employees[emp]) for emp in employees]))

# Add constraints based on the problem description
solver.add(f(employees["Y"]) > f(employees["T"]))
solver.add(f(employees["X"]) > f(employees["S"]))
solver.add(f(employees["R"]) > f(employees["Y"]))
solver.add(Or(f(employees["R"]) == 1, f(employees["R"]) == 2, f(employees["R"]) == 3, f(employees["R"]) == 4))

# Define answer choices
answer_choices = [
    {"Y": 1, "S": 2, "V": 3, "R": 4, "T": 5, "X": 6},
    {"V": 1, "T": 2, "Y": 3, "S": 4, "R": 5, "X": 6},
    {"T": 1, "Y": 2, "X": 3, "R": 4, "S": 5, "V": 6},
    {"T": 1, "R": 2, "Y": 3, "S": 4, "V": 5, "X": 6},
    {"S": 1, "T": 2, "Y": 3, "R": 4, "X": 5, "V": 6},
]

# Check each answer choice
for i, choice in enumerate(answer_choices):
    solver.push()
    for emp, space in choice.items():
        solver.add(f(employees[emp]) == space)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()