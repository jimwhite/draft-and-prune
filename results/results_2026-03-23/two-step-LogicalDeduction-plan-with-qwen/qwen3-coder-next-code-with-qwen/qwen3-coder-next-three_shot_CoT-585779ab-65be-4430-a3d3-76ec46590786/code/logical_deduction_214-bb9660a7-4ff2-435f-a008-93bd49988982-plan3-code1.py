from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["cardinal", "crow", "hummingbird", "blue jay", "owl", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The cardinal is to the right of the crow" → cardinal > crow
problem.addConstraint(lambda cardinal, crow: cardinal > crow, ["cardinal", "crow"])

# "The quail is the third from the left" → quail == 3
problem.addConstraint(lambda quail: quail == 3, ["quail"])

# "The owl is to the right of the robin" → owl > robin
problem.addConstraint(lambda owl, robin: owl > robin, ["owl", "robin"])

# "The hummingbird is to the right of the blue jay" → hummingbird > blue jay
problem.addConstraint(lambda hummingbird, blue_jay: hummingbird > blue_jay, ["hummingbird", "blue jay"])

# "The cardinal is the second from the left" → cardinal == 2
problem.addConstraint(lambda cardinal: cardinal == 2, ["cardinal"])

# "The owl is the third from the right" → position = 7 - 3 + 1 = 5
problem.addConstraint(lambda owl: owl == 5, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters
bird_to_choice = {
    "cardinal": "A",
    "crow": "B",
    "hummingbird": "C",
    "blue jay": "D",
    "owl": "E",
    "robin": "F",
    "quail": "G"
}

# Find the bird at position 2 and output its choice letter
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 2:
            print(bird_to_choice[bird])