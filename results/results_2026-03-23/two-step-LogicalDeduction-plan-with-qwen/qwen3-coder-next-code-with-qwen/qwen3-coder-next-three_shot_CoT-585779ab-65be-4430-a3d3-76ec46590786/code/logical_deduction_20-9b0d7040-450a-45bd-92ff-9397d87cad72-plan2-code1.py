from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["blue jay", "raven", "crow", "falcon", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The crow is to the left of the quail: crow < quail
problem.addConstraint(lambda crow, quail: crow < quail, ("crow", "quail"))

# The falcon is the leftmost: falcon == 1
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# The blue jay is to the right of the quail: quail < blue jay
problem.addConstraint(lambda quail, blue_jay: quail < blue_jay, ("quail", "blue jay"))

# The raven is the second from the left: raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
# Check each solution to find which bird has position 2
for solution in solutions:
    # Create mapping from choice letter to bird name as per choices
    choices = {
        "A": "blue jay",
        "B": "raven",
        "C": "crow",
        "D": "falcon",
        "E": "quail"
    }
    
    # Find which bird is at position 2
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)