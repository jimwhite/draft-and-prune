from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["cardinal", "crow", "falcon", "robin", "blue jay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the right of the cardinal" → robin > cardinal
problem.addConstraint(lambda robin, cardinal: robin > cardinal, ["robin", "cardinal"])

# "The cardinal is to the right of the blue jay" → cardinal > blue_jay
problem.addConstraint(lambda cardinal, blue_jay: cardinal > blue_jay, ["cardinal", "blue jay"])

# "The blue jay is the second from the left" → blue_jay == 2
problem.addConstraint(lambda blue_jay: blue_jay == 2, ["blue jay"])

# "The crow is the rightmost" → crow == 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "falcon",
    "D": "robin",
    "E": "blue jay"
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)