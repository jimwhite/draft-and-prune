from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["owl", "crow", "raven", "robin", "cardinal"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The raven is the second from the left"
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The raven is to the right of the owl" -> owl < raven
problem.addConstraint(lambda owl, raven: owl < raven, ["owl", "raven"])

# "The robin is the second from the right"
problem.addConstraint(lambda robin: robin == 4, ["robin"])

# "The robin is to the left of the crow" -> robin < crow
problem.addConstraint(lambda robin, crow: robin < crow, ["robin", "crow"])

# Solve the problem
solutions = problem.getSolutions()

# Identify which bird is at position 2 (second from the left)
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 2:
            print("C")
            break