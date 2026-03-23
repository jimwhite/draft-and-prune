from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["quail", "raven", "hummingbird", "robin", "falcon", "owl", "bluejay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# 1. The blue jay is to the left of the falcon → bluejay < falcon
problem.addConstraint(lambda bluejay, falcon: bluejay < falcon, ("bluejay", "falcon"))

# 2. The blue jay is the second from the right → bluejay == 6
problem.addConstraint(lambda bluejay: bluejay == 6, ("bluejay",))

# 3. The raven is to the left of the robin → raven < robin
problem.addConstraint(lambda raven, robin: raven < robin, ("raven", "robin"))

# 4. The owl is the third from the right → owl == 5
problem.addConstraint(lambda owl: owl == 5, ("owl",))

# 5. The hummingbird is to the left of the quail → hummingbird < quail
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ("hummingbird", "quail"))

# 6. The raven is the third from the left → raven == 3
problem.addConstraint(lambda raven: raven == 3, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters
choices = {
    "A": "quail",
    "B": "raven",
    "C": "hummingbird",
    "D": "robin",
    "E": "falcon",
    "F": "owl",
    "G": "bluejay"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)