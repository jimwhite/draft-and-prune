from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["cardinal", "crow", "falcon", "robin", "blue jay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the right of the cardinal" → robin > cardinal
problem.addConstraint(lambda robin, cardinal: robin > cardinal, ["robin", "cardinal"])

# 3. "The cardinal is to the right of the blue jay" → cardinal > blue jay
problem.addConstraint(lambda cardinal, blue_jay: cardinal > blue_jay, ["cardinal", "blue jay"])

# 4. "The blue jay is the second from the left" → blue_jay == 2
problem.addConstraint(lambda blue_jay: blue_jay == 2, ["blue jay"])

# 5. "The crow is the rightmost" → crow == 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "falcon",
    "D": "robin",
    "E": "blue jay"
}

# Find which bird is at position 1 (leftmost) and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)