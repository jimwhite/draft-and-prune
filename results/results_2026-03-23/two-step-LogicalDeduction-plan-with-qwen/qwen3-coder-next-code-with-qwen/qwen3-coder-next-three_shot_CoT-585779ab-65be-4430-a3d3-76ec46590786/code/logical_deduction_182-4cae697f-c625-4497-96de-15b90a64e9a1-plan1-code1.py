from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "hummingbird", "quail", "owl", "crow", "robin", "cardinal"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The cardinal is the second from the right (position 6)
problem.addConstraint(lambda cardinal: cardinal == 6, ["cardinal"])

# The hawk is the rightmost (position 7)
problem.addConstraint(lambda hawk: hawk == 7, ["hawk"])

# The owl is to the left of the hummingbird (owl < hummingbird)
problem.addConstraint(lambda owl, hummingbird: owl < hummingbird, ["owl", "hummingbird"])

# The robin is to the left of the quail (robin < quail)
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# The owl is to the right of the crow (owl > crow)
problem.addConstraint(lambda owl, crow: owl > crow, ["owl", "crow"])

# The robin is the fourth from the left (position 4)
problem.addConstraint(lambda robin: robin == 4, ["robin"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "hawk",
    "B": "hummingbird",
    "C": "quail",
    "D": "owl",
    "E": "crow",
    "F": "robin",
    "G": "cardinal"
}

# Find the leftmost bird (position 1) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)