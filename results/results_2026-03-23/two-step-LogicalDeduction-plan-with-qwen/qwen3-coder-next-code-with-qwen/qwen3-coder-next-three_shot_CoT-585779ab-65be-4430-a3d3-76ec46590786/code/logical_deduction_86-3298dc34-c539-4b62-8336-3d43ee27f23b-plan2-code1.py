from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=last)
golfers = ["Eve", "Eli", "Joe", "Rob", "Mya"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Rob finished above Mya: Rob < Mya
problem.addConstraint(lambda Rob, Mya: Rob < Mya, ["Rob", "Mya"])

# Eve finished first: Eve == 1
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# Joe finished above Eli: Joe < Eli
problem.addConstraint(lambda Joe, Eli: Joe < Eli, ["Joe", "Eli"])

# Joe finished below Mya: Mya < Joe
problem.addConstraint(lambda Mya, Joe: Mya < Joe, ["Mya", "Joe"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfer names
choices = {
    "A": "Eve",
    "B": "Eli",
    "C": "Joe",
    "D": "Rob",
    "E": "Mya"
}

# Find which golfer finished last (position 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)