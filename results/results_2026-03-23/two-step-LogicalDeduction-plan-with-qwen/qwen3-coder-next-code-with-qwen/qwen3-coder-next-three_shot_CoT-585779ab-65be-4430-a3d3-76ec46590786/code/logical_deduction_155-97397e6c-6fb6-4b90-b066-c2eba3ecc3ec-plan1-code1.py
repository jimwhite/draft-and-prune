from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven bird variables and domain (positions 1 to 7)
birds = ["cardinal", "crow", "hummingbird", "blue jay", "owl", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint to ensure each bird is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add the positional constraints based on the problem description:
# 1. "The cardinal is to the right of the crow" → cardinal > crow
problem.addConstraint(lambda cardinal, crow: cardinal > crow, ["cardinal", "crow"])

# 2. "The quail is the third from the left" → quail == 3
problem.addConstraint(lambda quail: quail == 3, ["quail"])

# 3. "The owl is to the right of the robin" → owl > robin
problem.addConstraint(lambda owl, robin: owl > robin, ["owl", "robin"])

# 4. "The hummingbird is to the right of the blue jay" → hummingbird > blue jay
problem.addConstraint(lambda hummingbird, blue_jay: hummingbird > blue_jay, ["hummingbird", "blue jay"])

# 5. "The cardinal is the second from the left" → cardinal == 2
problem.addConstraint(lambda cardinal: cardinal == 2, ["cardinal"])

# 6. "The owl is the third from the right" → owl == 5 (since 7-3+1=5)
problem.addConstraint(lambda owl: owl == 5, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    'A': "cardinal",
    'B': "crow",
    'C': "hummingbird",
    'D': "blue jay",
    'E': "owl",
    'F': "robin",
    'G': "quail"
}

# Find which bird is at position 1 (leftmost) and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)