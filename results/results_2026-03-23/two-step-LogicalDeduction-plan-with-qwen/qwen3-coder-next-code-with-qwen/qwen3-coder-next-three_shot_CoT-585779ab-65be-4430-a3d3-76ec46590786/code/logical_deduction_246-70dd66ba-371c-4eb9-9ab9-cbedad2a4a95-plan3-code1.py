from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["owl", "crow", "cardinal"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The crow is to the left of the owl"
problem.addConstraint(lambda crow, owl: crow < owl, ["crow", "owl"])

# "The owl is the second from the left"
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which bird is rightmost (position 3)
choices = {
    "A": "owl",
    "B": "crow",
    "C": "cardinal"
}

# Find the bird at position 3 and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)