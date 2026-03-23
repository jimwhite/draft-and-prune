from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "bluejay", "crow"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# 1. The quail is to the left of the owl.
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# 2. The owl is the second from the left.
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# 3. The crow is to the right of the falcon.
problem.addConstraint(lambda falcon, crow: falcon < crow, ["falcon", "crow"])

# 4. The blue jay is to the right of the hummingbird.
problem.addConstraint(lambda hummingbird, bluejay: hummingbird < bluejay, ["hummingbird", "bluejay"])

# 5. The hummingbird is to the right of the raven.
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ["raven", "hummingbird"])

# 6. The blue jay is to the left of the falcon.
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ["bluejay", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    'A': 'falcon',
    'B': 'owl',
    'C': 'quail',
    'D': 'raven',
    'E': 'hummingbird',
    'F': 'bluejay',
    'G': 'crow'
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)