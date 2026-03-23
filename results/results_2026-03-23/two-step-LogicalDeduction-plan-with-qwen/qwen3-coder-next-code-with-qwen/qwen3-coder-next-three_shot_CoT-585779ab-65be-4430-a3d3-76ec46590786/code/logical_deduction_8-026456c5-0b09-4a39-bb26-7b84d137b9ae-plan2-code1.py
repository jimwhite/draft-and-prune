from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
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

# Determine which bird is at position 5 (rightmost)
for solution in solutions:
    if solution["owl"] == 5:
        print("A")
    elif solution["robin"] == 5:
        print("B")
    elif solution["blue jay"] == 5:
        print("C")
    elif solution["hawk"] == 5:
        print("D")
    elif solution["hummingbird"] == 5:
        print("E")