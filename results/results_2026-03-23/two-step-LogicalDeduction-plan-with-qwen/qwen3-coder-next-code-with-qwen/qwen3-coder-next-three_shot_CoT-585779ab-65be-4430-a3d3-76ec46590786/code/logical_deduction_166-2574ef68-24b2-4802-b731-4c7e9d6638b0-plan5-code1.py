from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "blue_jay", "crow"]
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

# 5. "The blue jay is to the right of the hummingbird" → hummingbird < blue_jay
problem.addConstraint(lambda hummingbird, blue_jay: hummingbird < blue_jay, ("hummingbird", "blue_jay"))

# 6. "The hummingbird is to the right of the raven" → raven < hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ("raven", "hummingbird"))

# 7. "The blue jay is to the left of the falcon" → blue_jay < falcon
problem.addConstraint(lambda blue_jay, falcon: blue_jay < falcon, ("blue_jay", "falcon"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "falcon",
    "B": "owl",
    "C": "quail",
    "D": "raven",
    "E": "hummingbird",
    "F": "blue_jay",
    "G": "crow"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)