from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hummingbird", "cardinal", "blue jay", "owl", "raven", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The hummingbird is to the left of the quail"
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ["hummingbird", "quail"])

# "The robin is to the left of the cardinal"
problem.addConstraint(lambda robin, cardinal: robin < cardinal, ["robin", "cardinal"])

# "The blue jay is the leftmost"
problem.addConstraint(lambda blue_jay: blue_jay == 1, ["blue jay"])

# "The cardinal is the fourth from the left"
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The raven is the third from the right" (position 5 in a 7-position sequence)
problem.addConstraint(lambda raven: raven == 5, ["raven"])

# "The owl is the third from the left"
problem.addConstraint(lambda owl: owl == 3, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Get the unique solution
solution = solutions[0]

# Determine which bird is at position 1 (leftmost)
leftmost_bird = None
for bird, pos in solution.items():
    if pos == 1:
        leftmost_bird = bird
        break

# Map the bird to the corresponding choice letter
bird_to_choice = {
    "hummingbird": "A",
    "cardinal": "B",
    "blue jay": "C",
    "owl": "D",
    "raven": "E",
    "quail": "F",
    "robin": "G"
}

# Print the correct choice letter
print(bird_to_choice[leftmost_bird])