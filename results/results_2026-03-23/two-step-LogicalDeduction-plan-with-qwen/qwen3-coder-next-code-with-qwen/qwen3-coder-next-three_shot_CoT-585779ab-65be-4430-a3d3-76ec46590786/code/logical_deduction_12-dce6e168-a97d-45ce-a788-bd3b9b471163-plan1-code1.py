from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Eve", "Rob", "Ana", "Eli", "Mya"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Eve finished first (position 1)
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# Rob finished second (position 2)
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Eli finished below Mya (Eli's position > Mya's position)
problem.addConstraint(lambda Eli, Mya: Eli > Mya, ["Eli", "Mya"])

# Ana finished below Eli (Ana's position > Eli's position)
problem.addConstraint(lambda Ana, Eli: Ana > Eli, ["Ana", "Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Eve",
    "B": "Rob",
    "C": "Ana",
    "D": "Eli",
    "E": "Mya"
}

# Find which golfer has position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)