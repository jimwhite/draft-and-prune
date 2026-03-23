from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Joe", "Eli", "Ada", "Mel", "Eve", "Rob", "Ana"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished first
problem.addConstraint(lambda Joe: Joe == 1, ["Joe"])

# Mel finished second-to-last (position 6)
problem.addConstraint(lambda Mel: Mel == 6, ["Mel"])

# Rob finished above Eve (Rob < Eve)
problem.addConstraint(lambda Rob, Eve: Rob < Eve, ["Rob", "Eve"])

# Mel finished above Eli (Mel < Eli)
problem.addConstraint(lambda Mel, Eli: Mel < Eli, ["Mel", "Eli"])

# Rob finished below Ada (Ada < Rob)
problem.addConstraint(lambda Ada, Rob: Ada < Rob, ["Ada", "Rob"])

# Eve finished fourth
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Joe",
    "B": "Eli",
    "C": "Ada",
    "D": "Mel",
    "E": "Eve",
    "F": "Rob",
    "G": "Ana"
}

# Find who finished fourth (position 4)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)