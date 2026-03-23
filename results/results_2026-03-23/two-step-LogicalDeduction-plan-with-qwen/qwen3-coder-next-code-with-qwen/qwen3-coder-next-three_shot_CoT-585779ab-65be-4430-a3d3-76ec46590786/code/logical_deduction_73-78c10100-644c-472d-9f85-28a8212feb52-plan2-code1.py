from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["falcon", "raven", "cardinal", "hawk", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statement
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The cardinal is the second from the right" → position 4
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# 3. "The hawk is to the right of the falcon" → falcon < hawk
problem.addConstraint(lambda falcon, hawk: falcon < hawk, ["falcon", "hawk"])

# 4. "The raven is the second from the left" → position 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# 5. "The crow is the rightmost" → position 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for checking "second from the left" (position 2)
choices = {
    "A": "falcon",
    "B": "raven",
    "C": "cardinal",
    "D": "hawk",
    "E": "crow"
}

# Find which bird is at position 2 and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)