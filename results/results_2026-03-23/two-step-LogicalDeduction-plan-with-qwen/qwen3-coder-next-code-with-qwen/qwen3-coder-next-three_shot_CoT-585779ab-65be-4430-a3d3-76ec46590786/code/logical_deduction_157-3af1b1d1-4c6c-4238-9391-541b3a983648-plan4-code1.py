from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven birds as variables (using single words without spaces)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "bluejay", "crow"]

# Define domain as positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraint that all birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
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

# Map choice letters to bird names
choices = {
    "A": "falcon",
    "B": "owl",
    "C": "quail",
    "D": "raven",
    "E": "hummingbird",
    "F": "bluejay",
    "G": "crow"
}

# Find which bird is in position 4 (fourth from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)