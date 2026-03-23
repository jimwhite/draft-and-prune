from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["bluejay", "cardinal", "hawk", "hummingbird", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The quail is to the left of the blue jay" -> quail < bluejay
problem.addConstraint(lambda quail, bluejay: quail < bluejay, ["quail", "bluejay"])

# "The cardinal is the third from the left" -> cardinal == 3
problem.addConstraint(lambda cardinal: cardinal == 3, ["cardinal"])

# "The quail is the second from the left" -> quail == 2
problem.addConstraint(lambda quail: quail == 2, ["quail"])

# "The blue jay is to the left of the hummingbird" -> bluejay < hummingbird
problem.addConstraint(lambda bluejay, hummingbird: bluejay < hummingbird, ["bluejay", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for position 3
choices = {
    "A": "bluejay",
    "B": "cardinal",
    "C": "hawk",
    "D": "hummingbird",
    "E": "quail"
}

# Find which bird is at position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)