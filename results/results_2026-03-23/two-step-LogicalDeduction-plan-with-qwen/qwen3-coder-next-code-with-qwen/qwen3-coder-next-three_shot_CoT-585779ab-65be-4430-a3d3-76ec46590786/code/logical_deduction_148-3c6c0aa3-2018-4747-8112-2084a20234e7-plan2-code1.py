from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "bluejay", "crow"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The quail is to the left of the owl" → quail < owl
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# "The owl is the second from the left" → owl == 2
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# "The crow is to the right of the falcon" → falcon < crow
problem.addConstraint(lambda falcon, crow: falcon < crow, ["falcon", "crow"])

# "The blue jay is to the right of the hummingbird" → hummingbird < bluejay
problem.addConstraint(lambda hummingbird, bluejay: hummingbird < bluejay, ["hummingbird", "bluejay"])

# "The hummingbird is to the right of the raven" → raven < hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ["raven", "hummingbird"])

# "The blue jay is to the left of the falcon" → bluejay < falcon
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ["bluejay", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map bird names to choice letters
bird_to_choice = {
    "falcon": "A",
    "owl": "B",
    "quail": "C",
    "raven": "D",
    "hummingbird": "E",
    "bluejay": "F",
    "crow": "G"
}

# Find the bird at position 2 and print its corresponding choice letter
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 2:
            print(bird_to_choice[bird])