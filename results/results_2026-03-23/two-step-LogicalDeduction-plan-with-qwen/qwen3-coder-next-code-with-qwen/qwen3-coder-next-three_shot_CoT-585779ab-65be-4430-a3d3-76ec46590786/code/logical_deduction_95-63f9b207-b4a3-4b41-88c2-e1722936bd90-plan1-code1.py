from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["bluejay", "cardinal", "hawk", "hummingbird", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The quail is the second from the left" → position 2
problem.addConstraint(lambda quail: quail == 2, ["quail"])

# 3. "The cardinal is the third from the left" → position 3
problem.addConstraint(lambda cardinal: cardinal == 3, ["cardinal"])

# 4. "The quail is to the left of the blue jay" → quail < bluejay
problem.addConstraint(lambda quail, bluejay: quail < bluejay, ["quail", "bluejay"])

# 5. "The blue jay is to the left of the hummingbird" → bluejay < hummingbird
problem.addConstraint(lambda bluejay, hummingbird: bluejay < hummingbird, ["bluejay", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "bluejay",
    "B": "cardinal",
    "C": "hawk",
    "D": "hummingbird",
    "E": "quail"
}

# Find which bird is at position 1 (leftmost) and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)