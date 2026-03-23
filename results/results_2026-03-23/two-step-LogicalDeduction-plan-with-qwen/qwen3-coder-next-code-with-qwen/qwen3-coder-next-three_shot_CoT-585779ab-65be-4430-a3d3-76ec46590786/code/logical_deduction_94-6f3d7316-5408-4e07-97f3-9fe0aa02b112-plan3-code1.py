from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["quail", "hummingbird", "blue_jay", "hawk", "robin"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The robin is the second from the left → robin == 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# The quail is the leftmost → quail == 1
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# The blue jay is to the left of the hummingbird → blue_jay < hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue_jay", "hummingbird"])

# The hawk is the third from the left → hawk == 3
problem.addConstraint(lambda hawk: hawk == 3, ["hawk"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which statement is true, and choice A states "The quail is the leftmost."
# Since we have a constraint that enforces quail == 1, and the problem states statements are consistent,
# choice A must be true. We verify this by checking that in the solution, quail == 1.
for solution in solutions:
    if solution["quail"] == 1:
        print("A")