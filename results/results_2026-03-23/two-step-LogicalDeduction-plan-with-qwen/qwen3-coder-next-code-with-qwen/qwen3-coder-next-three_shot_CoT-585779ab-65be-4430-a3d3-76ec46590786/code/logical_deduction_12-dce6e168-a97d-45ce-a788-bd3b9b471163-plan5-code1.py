from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=fifth)
golfers = ["Eve", "Rob", "Ana", "Eli", "Mya"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Eli finished below Mya" → Mya's position < Eli's position
problem.addConstraint(lambda Mya, Eli: Mya < Eli, ["Mya", "Eli"])

# "Eve finished first" → Eve's position = 1
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# "Ana finished below Eli" → Eli's position < Ana's position
problem.addConstraint(lambda Eli, Ana: Eli < Ana, ["Eli", "Ana"])

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

# Find which golfer finished third (position = 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)