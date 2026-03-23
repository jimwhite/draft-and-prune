from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["bluejay", "owl", "hawk", "falcon", "hummingbird", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The hummingbird is to the left of the falcon"
problem.addConstraint(lambda hummingbird, falcon: hummingbird < falcon, ("hummingbird", "falcon"))

# "The owl is the second from the left"
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# "The robin is to the left of the hummingbird"
problem.addConstraint(lambda robin, hummingbird: robin < hummingbird, ("robin", "hummingbird"))

# "The quail is to the right of the falcon"
problem.addConstraint(lambda falcon, quail: falcon < quail, ("falcon", "quail"))

# "The robin is to the right of the owl"
problem.addConstraint(lambda owl, robin: owl < robin, ("owl", "robin"))

# "The blue jay is the third from the right" (position 5 in a 7-position sequence)
problem.addConstraint(lambda bluejay: bluejay == 5, ["bluejay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "bluejay",
    "B": "owl",
    "C": "hawk",
    "D": "falcon",
    "E": "hummingbird",
    "F": "robin",
    "G": "quail"
}

# Find the bird at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)