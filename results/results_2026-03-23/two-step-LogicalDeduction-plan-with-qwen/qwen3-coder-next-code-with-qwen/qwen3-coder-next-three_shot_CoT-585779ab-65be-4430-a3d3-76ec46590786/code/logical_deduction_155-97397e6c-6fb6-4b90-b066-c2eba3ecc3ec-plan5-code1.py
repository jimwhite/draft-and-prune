from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["cardinal", "crow", "hummingbird", "blue jay", "owl", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The cardinal is the second from the left" → cardinal == 2
problem.addConstraint(lambda cardinal: cardinal == 2, ["cardinal"])

# 2. "The quail is the third from the left" → quail == 3
problem.addConstraint(lambda quail: quail == 3, ["quail"])

# 3. "The cardinal is to the right of the crow" → crow < cardinal (crow < 2)
problem.addConstraint(lambda crow, cardinal: crow < cardinal, ["crow", "cardinal"])

# 4. "The owl is the third from the right" → position = 7 - 3 + 1 = 5, so owl == 5
problem.addConstraint(lambda owl: owl == 5, ["owl"])

# 5. "The owl is to the right of the robin" → robin < owl (robin < 5)
problem.addConstraint(lambda robin, owl: robin < owl, ["robin", "owl"])

# 6. "The hummingbird is to the right of the blue jay" → blue jay < hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "hummingbird",
    "D": "blue jay",
    "E": "owl",
    "F": "robin",
    "G": "quail"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)