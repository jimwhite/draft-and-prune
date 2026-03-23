from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "bluejay", "crow"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The quail is to the left of the owl" → quail < owl
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# 2. "The owl is the second from the left" → owl == 2
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# 3. "The crow is to the right of the falcon" → falcon < crow
problem.addConstraint(lambda falcon, crow: falcon < crow, ["falcon", "crow"])

# 4. "The blue jay is to the right of the hummingbird" → hummingbird < bluejay
problem.addConstraint(lambda hummingbird, bluejay: hummingbird < bluejay, ["hummingbird", "bluejay"])

# 5. "The hummingbird is to the right of the raven" → raven < hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ["raven", "hummingbird"])

# 6. "The blue jay is to the left of the falcon" → bluejay < falcon
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ["bluejay", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
# According to statement 2, owl should be at position 2, but let's verify with the solution
# Create mapping from choice letters to bird names as per choices list:
choices = {
    "A": "falcon",
    "B": "owl",
    "C": "quail",
    "D": "raven",
    "E": "hummingbird",
    "F": "bluejay",
    "G": "crow"
}

# Find the bird at position 2 in the solution
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)