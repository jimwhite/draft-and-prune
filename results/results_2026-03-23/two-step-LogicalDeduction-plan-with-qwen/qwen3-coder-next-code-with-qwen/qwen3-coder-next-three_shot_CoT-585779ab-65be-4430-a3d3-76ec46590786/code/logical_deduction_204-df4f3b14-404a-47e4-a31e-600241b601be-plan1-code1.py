from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["quail", "raven", "hummingbird", "robin", "falcon", "owl", "blue jay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The blue jay is to the left of the falcon"
problem.addConstraint(lambda blue_jay, falcon: blue_jay < falcon, ["blue jay", "falcon"])

# 2. "The blue jay is the second from the right" (position 6)
problem.addConstraint(lambda blue_jay: blue_jay == 6, ["blue jay"])

# 3. "The raven is to the left of the robin"
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])

# 4. "The owl is the third from the right" (position 5)
problem.addConstraint(lambda owl: owl == 5, ["owl"])

# 5. "The hummingbird is to the left of the quail"
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ["hummingbird", "quail"])

# 6. "The raven is the third from the left" (position 3)
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is fourth from the left (position 4)
choices = {
    "A": "quail",
    "B": "raven",
    "C": "hummingbird",
    "D": "robin",
    "E": "falcon",
    "F": "owl",
    "G": "blue jay"
}

# Find the bird at position 4 and print its corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)