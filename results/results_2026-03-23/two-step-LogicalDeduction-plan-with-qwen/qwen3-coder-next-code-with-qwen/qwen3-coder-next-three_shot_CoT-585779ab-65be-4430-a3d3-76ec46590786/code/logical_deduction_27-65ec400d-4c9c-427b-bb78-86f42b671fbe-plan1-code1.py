from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["owl", "robin", "blue_jay", "hawk", "hummingbird"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The owl is the second from the right (position 4)
problem.addConstraint(lambda owl: owl == 4, ["owl"])

# The robin is the second from the left (position 2)
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# The robin is to the right of the blue jay (blue_jay < robin)
problem.addConstraint(lambda blue_jay, robin: blue_jay < robin, ["blue_jay", "robin"])

# The hummingbird is to the right of the hawk (hawk < hummingbird)
problem.addConstraint(lambda hawk, hummingbird: hawk < hummingbird, ["hawk", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "owl",
    "B": "robin",
    "C": "blue_jay",
    "D": "hawk",
    "E": "hummingbird"
}

# Find which bird is at position 1 (leftmost) and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)