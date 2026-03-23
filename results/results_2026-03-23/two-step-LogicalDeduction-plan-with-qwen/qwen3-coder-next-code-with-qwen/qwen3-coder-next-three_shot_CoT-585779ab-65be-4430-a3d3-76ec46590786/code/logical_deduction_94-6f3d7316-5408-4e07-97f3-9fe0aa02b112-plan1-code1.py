from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["quail", "hummingbird", "blue jay", "hawk", "robin"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# 3. "The quail is the leftmost" → quail == 1
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# 4. "The blue jay is to the left of the hummingbird" → blue jay < hummingbird
problem.addConstraint(lambda bj, hum: bj < hum, ["blue jay", "hummingbird"])

# 5. "The hawk is the third from the left" → hawk == 3
problem.addConstraint(lambda hawk: hawk == 3, ["hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to the bird they claim is leftmost (position 1)
choices = {
    "A": "quail",
    "B": "hummingbird",
    "C": "blue jay",
    "D": "hawk",
    "E": "robin"
}

# Find which bird is at position 1 in the solution
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)