from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["blue jay", "cardinal", "quail"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The cardinal is to the right of the quail" -> cardinal > quail
problem.addConstraint(lambda cardinal, quail: cardinal > quail, ["cardinal", "quail"])

# "The quail is to the right of the blue jay" -> quail > blue_jay
problem.addConstraint(lambda quail, blue_jay: quail > blue_jay, ["quail", "blue jay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "blue jay",
    "B": "cardinal",
    "C": "quail"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)