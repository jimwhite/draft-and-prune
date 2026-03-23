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

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which bird is rightmost (position 3)
for solution in solutions:
    if solution["owl"] == 2:
        # Find which bird is at position 3
        for bird in birds:
            if solution[bird] == 3:
                if bird == "crow":
                    print("B")
                elif bird == "cardinal":
                    print("C")
                break