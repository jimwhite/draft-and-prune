from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["crow", "falcon", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The crow is to the left of the falcon" => crow < falcon
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# 3. "The hummingbird is to the left of the crow" => hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ["hummingbird", "crow"])

# Get the solution
solutions = problem.getSolutions()

# Map birds to choice letters for the rightmost position (position 3)
bird_to_choice = {
    "crow": "A",
    "falcon": "B",
    "hummingbird": "C"
}

# Find which bird is at position 3 (rightmost)
for solution in solutions:
    for bird, choice in bird_to_choice.items():
        if solution[bird] == 3:
            print(choice)