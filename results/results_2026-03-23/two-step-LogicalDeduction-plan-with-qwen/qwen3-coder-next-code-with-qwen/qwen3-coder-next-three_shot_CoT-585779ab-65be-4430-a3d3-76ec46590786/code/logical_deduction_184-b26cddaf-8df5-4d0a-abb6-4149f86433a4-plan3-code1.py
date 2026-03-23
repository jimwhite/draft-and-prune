from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Joe", "Eli", "Ada", "Mel", "Eve", "Rob", "Ana"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
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
    'A': 'Joe',
    'B': 'Eli',
    'C': 'Ada',
    'D': 'Mel',
    'E': 'Eve',
    'F': 'Rob',
    'G': 'Ana'
}

# Find who finished last (position 7)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 7:
            print(letter)