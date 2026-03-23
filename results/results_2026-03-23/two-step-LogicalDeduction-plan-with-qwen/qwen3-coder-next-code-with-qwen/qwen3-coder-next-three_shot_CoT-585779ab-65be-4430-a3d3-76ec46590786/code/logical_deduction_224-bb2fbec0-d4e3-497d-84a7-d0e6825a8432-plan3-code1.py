from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["quail", "raven", "hummingbird", "robin", "falcon", "owl", "bluejay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The blue jay is to the left of the falcon" → bluejay < falcon
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ("bluejay", "falcon"))

# "The blue jay is the second from the right" → bluejay == 6
problem.addConstraint(lambda bluejay: bluejay == 6, ("bluejay",))

# "The raven is to the left of the robin" → raven < robin
problem.addConstraint(lambda raven, robin: raven < robin, ("raven", "robin"))

# "The owl is the third from the right" → owl == 5
problem.addConstraint(lambda owl: owl == 5, ("owl",))

# "The hummingbird is to the left of the quail" → hummingbird < quail
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ("hummingbird", "quail"))

# "The raven is the third from the left" → raven == 3
problem.addConstraint(lambda raven: raven == 3, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters for position 7 (rightmost)
bird_to_choice = {
    "quail": "A",
    "raven": "B",
    "hummingbird": "C",
    "robin": "D",
    "falcon": "E",
    "owl": "F",
    "bluejay": "G"
}

# Find the bird at position 7 and print its choice letter
for solution in solutions:
    for bird, choice in bird_to_choice.items():
        if solution[bird] == 7:
            print(choice)