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

# "Eli finished below Mya" → Eli's position > Mya's position
problem.addConstraint(lambda Eli, Mya: Eli > Mya, ["Eli", "Mya"])

# "Eve finished first" → Eve's position = 1
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# "Ana finished below Eli" → Ana's position > Eli's position
problem.addConstraint(lambda Ana, Eli: Ana > Eli, ["Ana", "Eli"])

# "Rob finished second" → Rob's position = 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Eve",
    "B": "Rob",
    "C": "Ana",
    "D": "Eli",
    "E": "Mya"
}

# Find who finished third (position = 3)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)