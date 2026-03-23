from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["owl", "robin", "bluejay", "hawk", "hummingbird"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The owl is the second from the right" → position 4
problem.addConstraint(lambda owl: owl == 4, ["owl"])

# "The robin is the second from the left" → position 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# "The robin is to the right of the blue jay" → bluejay < robin
problem.addConstraint(lambda bluejay, robin: bluejay < robin, ["bluejay", "robin"])

# "The hummingbird is to the right of the hawk" → hawk < hummingbird
problem.addConstraint(lambda hawk, hummingbird: hawk < hummingbird, ["hawk", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "owl",
    "B": "robin",
    "C": "bluejay",
    "D": "hawk",
    "E": "hummingbird"
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)