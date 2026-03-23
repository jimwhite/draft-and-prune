from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["quail", "raven", "hummingbird", "robin", "falcon", "owl", "bluejay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add position-based constraints
# "The blue jay is the second from the right" → position 6
problem.addConstraint(lambda bluejay: bluejay == 6, ["bluejay"])
# "The owl is the third from the right" → position 5
problem.addConstraint(lambda owl: owl == 5, ["owl"])
# "The raven is the third from the left" → position 3
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Add relative-order constraints
# "The blue jay is to the left of the falcon" → bluejay < falcon
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ["bluejay", "falcon"])
# "The raven is to the left of the robin" → raven < robin
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])
# "The hummingbird is to the left of the quail" → hummingbird < quail
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ["hummingbird", "quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "quail",
    "B": "raven",
    "C": "hummingbird",
    "D": "robin",
    "E": "falcon",
    "F": "owl",
    "G": "bluejay"
}

# Find the bird at position 7 (rightmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 7:
            print(letter)