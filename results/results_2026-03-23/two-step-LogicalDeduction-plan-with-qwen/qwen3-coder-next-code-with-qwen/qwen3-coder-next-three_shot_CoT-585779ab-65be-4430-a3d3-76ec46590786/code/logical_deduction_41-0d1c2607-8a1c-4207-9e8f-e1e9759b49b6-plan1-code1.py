from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["cardinal", "crow", "falcon", "robin", "bluejay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the right of the cardinal" → robin > cardinal
problem.addConstraint(lambda robin, cardinal: robin > cardinal, ["robin", "cardinal"])

# 3. "The cardinal is to the right of the blue jay" → cardinal > bluejay
problem.addConstraint(lambda cardinal, bluejay: cardinal > bluejay, ["cardinal", "bluejay"])

# 4. "The blue jay is the second from the left" → bluejay == 2
problem.addConstraint(lambda bluejay: bluejay == 2, ["bluejay"])

# 5. "The crow is the rightmost" → crow == 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "falcon",
    "D": "robin",
    "E": "bluejay"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)