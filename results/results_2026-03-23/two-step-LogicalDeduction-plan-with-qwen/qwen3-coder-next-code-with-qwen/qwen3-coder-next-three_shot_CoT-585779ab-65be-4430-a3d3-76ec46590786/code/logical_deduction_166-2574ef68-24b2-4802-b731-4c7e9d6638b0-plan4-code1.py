from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "blue_jay", "crow"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The quail is to the left of the owl" → quail < owl
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# "The owl is the second from the left" → owl == 2
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# "The crow is to the right of the falcon" → falcon < crow
problem.addConstraint(lambda falcon, crow: falcon < crow, ["falcon", "crow"])

# "The blue jay is to the right of the hummingbird" → hummingbird < blue_jay
problem.addConstraint(lambda hummingbird, blue_jay: hummingbird < blue_jay, ["hummingbird", "blue_jay"])

# "The hummingbird is to the right of the raven" → raven < hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ["raven", "hummingbird"])

# "The blue jay is to the left of the falcon" → blue_jay < falcon
problem.addConstraint(lambda blue_jay, falcon: blue_jay < falcon, ["blue_jay", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters
bird_to_choice = {
    "falcon": "A",
    "owl": "B",
    "quail": "C",
    "raven": "D",
    "hummingbird": "E",
    "blue_jay": "F",
    "crow": "G"
}

# Find the bird at position 1 (leftmost) and print its choice letter
for solution in solutions:
    for bird, position in solution.items():
        if position == 1:
            print(bird_to_choice[bird])