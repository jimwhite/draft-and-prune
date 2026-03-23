from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["owl", "crow", "raven", "robin", "cardinal"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The raven is the second from the left"
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The raven is to the right of the owl" -> owl < raven
problem.addConstraint(lambda owl, raven: owl < raven, ["owl", "raven"])

# "The robin is the second from the right" -> position 4
problem.addConstraint(lambda robin: robin == 4, ["robin"])

# "The robin is to the left of the crow" -> robin < crow
problem.addConstraint(lambda robin, crow: robin < crow, ["robin", "crow"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
choices = {
    "A": "owl",
    "B": "crow",
    "C": "raven",
    "D": "robin",
    "E": "cardinal"
}

# Find which bird is at position 2 and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)