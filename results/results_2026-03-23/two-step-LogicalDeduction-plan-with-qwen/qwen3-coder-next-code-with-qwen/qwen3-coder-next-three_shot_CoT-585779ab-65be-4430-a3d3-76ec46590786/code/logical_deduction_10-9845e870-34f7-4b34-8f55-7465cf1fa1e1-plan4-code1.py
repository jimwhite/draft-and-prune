from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["owl", "robin", "blue jay", "hawk", "hummingbird"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The owl is the second from the right (position 4)
problem.addConstraint(lambda owl: owl == 4, ["owl"])

# The robin is the second from the left (position 2)
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# The robin is to the right of the blue jay (blue_jay < robin)
problem.addConstraint(lambda blue_jay, robin: blue_jay < robin, ["blue jay", "robin"])

# The hummingbird is to the right of the hawk (hawk < hummingbird)
problem.addConstraint(lambda hawk, hummingbird: hawk < hummingbird, ["hawk", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
# According to the constraints, robin is fixed at position 2
# Let's verify by checking which bird has position 2 in the solution

for solution in solutions:
    # Find which bird is at position 2
    for bird, pos in solution.items():
        if pos == 2:
            # Map to the corresponding choice
            if bird == "owl":
                print("A")
            elif bird == "robin":
                print("B")
            elif bird == "blue jay":
                print("C")
            elif bird == "hawk":
                print("D")
            elif bird == "hummingbird":
                print("E")