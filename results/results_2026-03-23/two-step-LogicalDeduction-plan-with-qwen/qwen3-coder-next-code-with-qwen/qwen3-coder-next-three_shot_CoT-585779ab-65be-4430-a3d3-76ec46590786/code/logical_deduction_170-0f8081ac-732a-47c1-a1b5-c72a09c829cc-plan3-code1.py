from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "hummingbird", "falcon", "cardinal", "owl", "robin", "blue jay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The hummingbird is to the left of the owl"
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ["hummingbird", "owl"])

# "The robin is the rightmost"
problem.addConstraint(lambda robin: robin == 7, ["robin"])

# "The blue jay is to the left of the hawk"
problem.addConstraint(lambda blue_jay, hawk: blue_jay < hawk, ["blue jay", "hawk"])

# "The blue jay is the third from the left"
problem.addConstraint(lambda blue_jay: blue_jay == 3, ["blue jay"])

# "The falcon is the fourth from the left"
problem.addConstraint(lambda falcon: falcon == 4, ["falcon"])

# "The cardinal is the second from the right"
problem.addConstraint(lambda cardinal: cardinal == 6, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the right (position 6)
# Since cardinal == 6 is a constraint, D) The cardinal is the second from the right must be true
# We'll verify this by checking the solution, though it's guaranteed by constraints

for solution in solutions:
    # Check which bird is at position 6
    for letter, bird_name in [
        ("A", "hawk"),
        ("B", "hummingbird"),
        ("C", "falcon"),
        ("D", "cardinal"),
        ("E", "owl"),
        ("F", "robin"),
        ("G", "blue jay")
    ]:
        if solution[bird_name] == 6:
            print(letter)