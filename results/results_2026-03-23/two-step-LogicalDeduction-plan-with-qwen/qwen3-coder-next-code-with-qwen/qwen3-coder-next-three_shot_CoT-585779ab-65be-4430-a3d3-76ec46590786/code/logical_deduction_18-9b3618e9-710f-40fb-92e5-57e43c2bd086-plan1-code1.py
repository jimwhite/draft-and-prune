from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["hawk", "raven", "robin", "hummingbird", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is the leftmost" → robin == 1
problem.addConstraint(lambda robin: robin == 1, ["robin"])

# "The raven is the second from the left" → raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The hawk is the second from the right" → hawk == 4
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# "The crow is the third from the left" → crow == 3
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is the second from the right (position 4)
# According to our constraints, hawk == 4, so choice A should be correct
# Let's verify by checking the solution

for solution in solutions:
    # Find which bird is at position 4
    for bird, pos in solution.items():
        if pos == 4:
            # Match with choices
            if bird == "hawk":
                print("A")
            break