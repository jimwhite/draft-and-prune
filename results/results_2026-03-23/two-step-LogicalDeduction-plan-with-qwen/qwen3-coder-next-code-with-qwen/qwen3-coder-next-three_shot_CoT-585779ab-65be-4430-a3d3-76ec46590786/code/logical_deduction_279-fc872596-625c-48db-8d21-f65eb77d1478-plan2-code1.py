from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["bluejay", "cardinal", "quail"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The cardinal is to the right of the quail" → cardinal > quail
problem.addConstraint(lambda cardinal, quail: cardinal > quail, ("cardinal", "quail"))

# 3. "The quail is to the right of the blue jay" → quail > bluejay
problem.addConstraint(lambda quail, bluejay: quail > bluejay, ("quail", "bluejay"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
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