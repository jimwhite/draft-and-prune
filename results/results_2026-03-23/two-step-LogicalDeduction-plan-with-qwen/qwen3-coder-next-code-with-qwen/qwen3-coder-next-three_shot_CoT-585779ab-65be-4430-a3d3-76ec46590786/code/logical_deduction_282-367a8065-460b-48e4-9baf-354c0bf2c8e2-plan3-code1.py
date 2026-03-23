from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["quail", "owl", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The quail is to the left of the owl: quail < owl
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# The owl is to the left of the hummingbird: owl < hummingbird
problem.addConstraint(lambda owl, hummingbird: owl < hummingbird, ["owl", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Determine the correct answer based on which bird is rightmost (position 3)
choices = {
    "A": "quail",
    "B": "owl",
    "C": "hummingbird"
}

# Find which bird is at position 3 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)