from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The raven is to the left of the hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ("raven", "hummingbird"))

# The hawk is to the left of the owl
problem.addConstraint(lambda hawk, owl: hawk < owl, ("hawk", "owl"))

# The cardinal is to the left of the hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ("cardinal", "hawk"))

# The raven is the second from the right (position 4)
problem.addConstraint(lambda raven: raven == 4, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters
bird_to_choice = {
    "cardinal": "A",
    "hawk": "B",
    "hummingbird": "C",
    "raven": "D",
    "owl": "E"
}

# Find the bird at position 5 (rightmost)
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 5:
            print(bird_to_choice[bird])