from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three birds
birds = ["quail", "owl", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The quail is to the left of the owl"
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# "The owl is to the left of the hummingbird"
problem.addConstraint(lambda owl, hummingbird: owl < hummingbird, ["owl", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "quail",
    "B": "owl",
    "C": "hummingbird"
}

# Find which bird is rightmost (position 3)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)