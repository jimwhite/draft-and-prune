from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Joe", "Ana", "Amy", "Mya", "Eve"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished last (position 5)
problem.addConstraint(lambda Joe: Joe == 5, ["Joe"])

# Ana finished second (position 2)
problem.addConstraint(lambda Ana: Ana == 2, ["Ana"])

# Mya finished second-to-last (position 4)
problem.addConstraint(lambda Mya: Mya == 4, ["Mya"])

# Eve finished below Amy (Eve's position > Amy's position)
problem.addConstraint(lambda Amy, Eve: Amy < Eve, ["Amy", "Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Ana",
    "C": "Amy",
    "D": "Mya",
    "E": "Eve"
}

# Find which golfer finished first (position 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)