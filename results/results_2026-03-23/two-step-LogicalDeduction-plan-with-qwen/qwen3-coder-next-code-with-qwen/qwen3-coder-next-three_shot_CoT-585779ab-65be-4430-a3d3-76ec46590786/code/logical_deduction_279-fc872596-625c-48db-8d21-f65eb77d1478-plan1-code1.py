from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["bluejay", "cardinal", "quail"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The quail is to the right of the blue jay" -> bluejay < quail
problem.addConstraint(lambda bluejay, quail: bluejay < quail, ("bluejay", "quail"))

# "The cardinal is to the right of the quail" -> quail < cardinal
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ("quail", "cardinal"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "bluejay",
    "B": "cardinal",
    "C": "quail"
}

# Find which bird is in position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)