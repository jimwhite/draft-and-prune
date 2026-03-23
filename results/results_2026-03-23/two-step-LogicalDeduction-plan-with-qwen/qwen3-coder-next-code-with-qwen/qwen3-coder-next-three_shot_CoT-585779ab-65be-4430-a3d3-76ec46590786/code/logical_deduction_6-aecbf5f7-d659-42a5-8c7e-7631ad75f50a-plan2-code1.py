from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1-5)
birds = ["crow", "robin", "quail", "bluejay", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the left of the quail"
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# "The falcon is the third from the left"
problem.addConstraint(lambda falcon: falcon == 3, ["falcon"])

# "The crow is to the left of the falcon"
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# "The blue jay is the leftmost"
problem.addConstraint(lambda bluejay: bluejay == 1, ["bluejay"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters for the question about who is third from left (position 3)
bird_to_choice = {
    "crow": "A",
    "robin": "B",
    "quail": "C",
    "bluejay": "D",
    "falcon": "E"
}

# Find which bird is at position 3 and print its corresponding choice letter
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 3:
            print(bird_to_choice[bird])