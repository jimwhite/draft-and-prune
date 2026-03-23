from constraint import *

# Initialize the problem
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

# Solve and find the rightmost bird
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "owl",
    "B": "crow",
    "C": "cardinal"
}

# Find which bird is at position 3 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)