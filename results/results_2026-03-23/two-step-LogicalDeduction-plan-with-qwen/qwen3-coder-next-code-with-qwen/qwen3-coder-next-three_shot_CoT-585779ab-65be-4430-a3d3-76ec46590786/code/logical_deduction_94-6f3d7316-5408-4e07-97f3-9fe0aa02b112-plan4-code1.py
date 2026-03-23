from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["quail", "hummingbird", "blue jay", "hawk", "robin"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The robin is the second from the left (position 2)
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# The quail is the leftmost (position 1)
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# The blue jay is to the left of the hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])

# The hawk is the third from the left (position 3)
problem.addConstraint(lambda hawk: hawk == 3, ["hawk"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is the leftmost (position 1)
# According to constraints, quail must be at position 1
# Let's verify programmatically by checking the solution

for solution in solutions:
    for letter, bird_name in [("A", "quail"), ("B", "hummingbird"), ("C", "blue jay"), ("D", "hawk"), ("E", "robin")]:
        if solution[bird_name] == 1:
            print(letter)