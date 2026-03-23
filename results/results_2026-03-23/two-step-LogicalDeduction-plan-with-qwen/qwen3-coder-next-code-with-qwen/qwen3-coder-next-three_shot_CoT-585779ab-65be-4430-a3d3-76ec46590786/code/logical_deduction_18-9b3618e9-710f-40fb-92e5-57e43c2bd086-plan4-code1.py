from constraint import *

# Set up the problem
problem = Problem()

# Define variables and domain
birds = ["hawk", "raven", "robin", "hummingbird", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add positional constraints
problem.addConstraint(lambda robin: robin == 1, ["robin"])
problem.addConstraint(lambda raven: raven == 2, ["raven"])
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "hawk",
    "B": "raven",
    "C": "robin",
    "D": "hummingbird",
    "E": "crow"
}

# Find which bird is at position 4 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)