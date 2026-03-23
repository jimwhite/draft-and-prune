from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1-5, where 1 is leftmost)
birds = ["quail", "hummingbird", "bluejay", "hawk", "robin"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The robin is the second from the left
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# The quail is the leftmost
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# The blue jay is to the left of the hummingbird
problem.addConstraint(lambda bluejay, hummingbird: bluejay < hummingbird, ["bluejay", "hummingbird"])

# The hawk is the third from the left
problem.addConstraint(lambda hawk: hawk == 3, ["hawk"])

# Solve for solutions
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "quail",
    "B": "hummingbird",
    "C": "bluejay",
    "D": "hawk",
    "E": "robin"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)