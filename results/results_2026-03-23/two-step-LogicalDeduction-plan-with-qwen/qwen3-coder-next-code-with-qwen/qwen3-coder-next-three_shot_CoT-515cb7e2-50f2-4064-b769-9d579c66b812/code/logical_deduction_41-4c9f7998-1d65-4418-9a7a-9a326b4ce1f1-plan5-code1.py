from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["cardinal", "crow", "falcon", "robin", "bluejay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the right of the cardinal" → robin > cardinal
problem.addConstraint(lambda robin, cardinal: robin > cardinal, ["robin", "cardinal"])

# "The cardinal is to the right of the blue jay" → cardinal > bluejay
problem.addConstraint(lambda cardinal, bluejay: cardinal > bluejay, ["cardinal", "bluejay"])

# "The blue jay is the second from the left" → bluejay == 2
problem.addConstraint(lambda bluejay: bluejay == 2, ["bluejay"])

# "The crow is the rightmost" → crow == 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "falcon",
    "D": "robin",
    "E": "bluejay"
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)