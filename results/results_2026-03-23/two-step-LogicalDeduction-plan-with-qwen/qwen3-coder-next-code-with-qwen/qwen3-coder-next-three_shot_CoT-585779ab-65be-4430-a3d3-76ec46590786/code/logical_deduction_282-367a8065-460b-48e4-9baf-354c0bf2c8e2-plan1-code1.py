from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["quail", "owl", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The quail is to the left of the owl: quail < owl
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# The owl is to the left of the hummingbird: owl < hummingbird
problem.addConstraint(lambda owl, hummingbird: owl < hummingbird, ["owl", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "quail",
    "B": "owl",
    "C": "hummingbird"
}

# Find which bird is in position 3 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)