from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["crow", "falcon", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The crow is to the left of the falcon" => crow < falcon
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# "The hummingbird is to the left of the crow" => hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ["hummingbird", "crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "hummingbird"
}

# Find which bird is rightmost (position 3)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)