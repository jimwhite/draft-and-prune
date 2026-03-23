from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Rob finished first
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])
# Eve finished last
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])
# Dan finished above Ada (Dan < Ada)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])
# Mel finished above Mya (Mel < Mya)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])
# Joe finished second-to-last (position 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])
# Mya finished third (position 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Mel",
    "C": "Mya",
    "D": "Eve",
    "E": "Rob",
    "F": "Ada",
    "G": "Dan"
}

# Find which golfer finished third (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)