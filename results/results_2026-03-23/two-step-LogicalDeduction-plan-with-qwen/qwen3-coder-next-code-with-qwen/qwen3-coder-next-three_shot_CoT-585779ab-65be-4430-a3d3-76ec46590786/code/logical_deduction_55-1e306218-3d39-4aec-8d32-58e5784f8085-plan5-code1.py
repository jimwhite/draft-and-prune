from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["crow", "falcon", "hawk", "robin", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the right of the falcon" → falcon < robin
problem.addConstraint(lambda falcon, robin: falcon < robin, ("falcon", "robin"))

# 3. "The quail is to the left of the hawk" → quail < hawk
problem.addConstraint(lambda quail, hawk: quail < hawk, ("quail", "hawk"))

# 4. "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ("robin",))

# 5. "The hawk is the second from the right" → hawk == 4
problem.addConstraint(lambda hawk: hawk == 4, ("hawk",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for the rightmost position (position 5)
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "hawk",
    "D": "robin",
    "E": "quail"
}

# Find which bird is at position 5 (rightmost) and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)