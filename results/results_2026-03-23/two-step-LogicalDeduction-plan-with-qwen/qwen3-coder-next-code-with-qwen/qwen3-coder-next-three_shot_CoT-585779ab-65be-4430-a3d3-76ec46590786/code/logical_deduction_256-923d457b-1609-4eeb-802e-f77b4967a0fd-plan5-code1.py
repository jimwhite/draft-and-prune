from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["Amy", "Ana", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Ana" means Amy's position > Ana's position
problem.addConstraint(lambda Amy, Ana: Amy > Ana, ["Amy", "Ana"])

# "Ana finished below Joe" means Ana's position > Joe's position
problem.addConstraint(lambda Ana, Joe: Ana > Joe, ["Ana", "Joe"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Amy",
    "B": "Ana",
    "C": "Joe"
}

# Find the golfer with position 1 (first place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)