from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["cardinal", "crow", "falcon", "robin", "blue_jay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the right of the cardinal"
problem.addConstraint(lambda robin, cardinal: robin > cardinal, ("robin", "cardinal"))

# "The cardinal is to the right of the blue jay"
problem.addConstraint(lambda cardinal, blue_jay: cardinal > blue_jay, ("cardinal", "blue_jay"))

# "The blue jay is the second from the left"
problem.addConstraint(lambda blue_jay: blue_jay == 2, ("blue_jay",))

# "The crow is the rightmost"
problem.addConstraint(lambda crow: crow == 5, ("crow",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "falcon",
    "D": "robin",
    "E": "blue_jay"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)