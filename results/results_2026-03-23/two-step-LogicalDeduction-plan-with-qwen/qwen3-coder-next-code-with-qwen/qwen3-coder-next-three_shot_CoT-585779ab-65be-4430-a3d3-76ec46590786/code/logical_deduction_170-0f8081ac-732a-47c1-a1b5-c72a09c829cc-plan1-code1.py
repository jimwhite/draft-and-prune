from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "hummingbird", "falcon", "cardinal", "owl", "robin", "bluejay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The hummingbird is to the left of the owl"
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ["hummingbird", "owl"])

# "The robin is the rightmost"
problem.addConstraint(lambda robin: robin == 7, ["robin"])

# "The blue jay is to the left of the hawk"
problem.addConstraint(lambda bluejay, hawk: bluejay < hawk, ["bluejay", "hawk"])

# "The blue jay is the third from the left"
problem.addConstraint(lambda bluejay: bluejay == 3, ["bluejay"])

# "The falcon is the fourth from the left"
problem.addConstraint(lambda falcon: falcon == 4, ["falcon"])

# "The cardinal is the second from the right"
problem.addConstraint(lambda cardinal: cardinal == 6, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hawk",
    "B": "hummingbird",
    "C": "falcon",
    "D": "cardinal",
    "E": "owl",
    "F": "robin",
    "G": "bluejay"
}

# Find which bird is at position 6 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)