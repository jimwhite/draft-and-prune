from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["cardinal", "crow", "hummingbird", "bluejay", "owl", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statement
# "The cardinal is to the right of the crow" → cardinal > crow
problem.addConstraint(lambda cardinal, crow: cardinal > crow, ["cardinal", "crow"])

# "The quail is the third from the left" → quail == 3
problem.addConstraint(lambda quail: quail == 3, ["quail"])

# "The owl is to the right of the robin" → owl > robin
problem.addConstraint(lambda owl, robin: owl > robin, ["owl", "robin"])

# "The hummingbird is to the right of the blue jay" → hummingbird > bluejay
problem.addConstraint(lambda hummingbird, bluejay: hummingbird > bluejay, ["hummingbird", "bluejay"])

# "The cardinal is the second from the left" → cardinal == 2
problem.addConstraint(lambda cardinal: cardinal == 2, ["cardinal"])

# "The owl is the third from the right" → position 5 (since 7-3+1=5)
problem.addConstraint(lambda owl: owl == 5, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "hummingbird",
    "D": "bluejay",
    "E": "owl",
    "F": "robin",
    "G": "quail"
}

# Find which bird is at position 5 (third from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)