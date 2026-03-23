from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["blue jay", "cardinal", "hawk", "hummingbird", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The quail is the second from the left" → quail == 2
problem.addConstraint(lambda quail: quail == 2, ["quail"])

# "The cardinal is the third from the left" → cardinal == 3
problem.addConstraint(lambda cardinal: cardinal == 3, ["cardinal"])

# "The quail is to the left of the blue jay" → quail < blue_jay
problem.addConstraint(lambda quail, blue_jay: quail < blue_jay, ["quail", "blue jay"])

# "The blue jay is to the left of the hummingbird" → blue_jay < hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which bird is at position 1 (leftmost)
for solution in solutions:
    # Map choice letters to bird names
    choices = {
        "A": "blue jay",
        "B": "cardinal",
        "C": "hawk",
        "D": "hummingbird",
        "E": "quail"
    }
    
    # Find which bird is at position 1
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)