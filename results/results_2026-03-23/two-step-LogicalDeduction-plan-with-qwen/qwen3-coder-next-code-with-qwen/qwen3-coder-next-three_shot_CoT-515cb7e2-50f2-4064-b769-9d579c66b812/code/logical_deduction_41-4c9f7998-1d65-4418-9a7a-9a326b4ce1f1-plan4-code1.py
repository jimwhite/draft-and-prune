from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["cardinal", "crow", "falcon", "robin", "bluejay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the right of the cardinal" → cardinal < robin
problem.addConstraint(lambda cardinal, robin: cardinal < robin, ["cardinal", "robin"])

# 3. "The cardinal is to the right of the blue jay" → bluejay < cardinal
problem.addConstraint(lambda bluejay, cardinal: bluejay < cardinal, ["bluejay", "cardinal"])

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

# Find which bird is at position 1 (leftmost) and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)