from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["blue_jay", "cardinal", "quail"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The cardinal is to the right of the quail" => cardinal > quail
problem.addConstraint(lambda cardinal, quail: cardinal > quail, ["cardinal", "quail"])

# "The quail is to the right of the blue jay" => quail > blue_jay
problem.addConstraint(lambda quail, blue_jay: quail > blue_jay, ["quail", "blue_jay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "blue_jay",
    "B": "cardinal",
    "C": "quail"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)