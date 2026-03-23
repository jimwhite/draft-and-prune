from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "bluejay", "crow"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The quail is to the left of the owl" → quail < owl
problem.addConstraint(lambda quail, owl: quail < owl, ("quail", "owl"))

# 3. "The owl is the second from the left" → owl == 2
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# 4. "The crow is to the right of the falcon" → falcon < crow
problem.addConstraint(lambda falcon, crow: falcon < crow, ("falcon", "crow"))

# 5. "The blue jay is to the right of the hummingbird" → hummingbird < bluejay
problem.addConstraint(lambda hummingbird, bluejay: hummingbird < bluejay, ("hummingbird", "bluejay"))

# 6. "The hummingbird is to the right of the raven" → raven < hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ("raven", "hummingbird"))

# 7. "The blue jay is to the left of the falcon" → bluejay < falcon
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ("bluejay", "falcon"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for position 4 (fourth from the left)
choices = {
    "A": "falcon",
    "B": "owl",
    "C": "quail",
    "D": "raven",
    "E": "hummingbird",
    "F": "bluejay",
    "G": "crow"
}

# Find the bird at position 4 and print its corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)