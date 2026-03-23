from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue_jay", "owl", "hawk", "falcon", "hummingbird", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The hummingbird is to the left of the falcon"
problem.addConstraint(lambda hummingbird, falcon: hummingbird < falcon, ["hummingbird", "falcon"])

# "The owl is the second from the left"
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# "The robin is to the left of the hummingbird"
problem.addConstraint(lambda robin, hummingbird: robin < hummingbird, ["robin", "hummingbird"])

# "The quail is to the right of the falcon"
problem.addConstraint(lambda falcon, quail: falcon < quail, ["falcon", "quail"])

# "The robin is to the right of the owl"
problem.addConstraint(lambda owl, robin: owl < robin, ["owl", "robin"])

# "The blue jay is the third from the right" -> position 5 in a 7-position line
problem.addConstraint(lambda blue_jay: blue_jay == 5, ["blue_jay"])

# Solve the problem
solutions = problem.getSolutions()

# Get the first (and only) solution
solution = solutions[0]

# Map choice letters to bird names
choices = {
    'A': 'blue_jay',
    'B': 'owl',
    'C': 'hawk',
    'D': 'falcon',
    'E': 'hummingbird',
    'F': 'robin',
    'G': 'quail'
}

# Find which bird is at position 1 (leftmost)
for letter, bird_name in choices.items():
    if solution[bird_name] == 1:
        print(letter)