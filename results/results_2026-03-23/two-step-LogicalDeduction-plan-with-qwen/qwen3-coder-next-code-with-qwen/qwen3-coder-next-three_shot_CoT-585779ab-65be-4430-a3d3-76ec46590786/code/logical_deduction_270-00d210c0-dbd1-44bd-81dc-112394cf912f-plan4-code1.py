from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three birds
birds = ["crow", "falcon", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The crow is to the left of the falcon: crow < falcon
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# The hummingbird is to the left of the crow: hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ["hummingbird", "crow"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "hummingbird"
}

# Find which bird is at position 3 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)