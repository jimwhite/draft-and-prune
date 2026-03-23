from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "crow", "owl", "raven", "falcon", "quail", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The hummingbird is the second from the left"
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# "The raven is the fourth from the left"
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# "The raven is to the right of the hawk"
problem.addConstraint(lambda hawk, raven: hawk < raven, ["hawk", "raven"])

# "The owl is to the right of the crow"
problem.addConstraint(lambda crow, owl: crow < owl, ["crow", "owl"])

# "The falcon is the rightmost"
problem.addConstraint(lambda falcon: falcon == 7, ["falcon"])

# "The hawk is to the right of the hummingbird"
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# "The quail is the second from the right"
problem.addConstraint(lambda quail: quail == 6, ["quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    'A': "quail",
    'B': "crow",
    'C': "owl",
    'D': "raven",
    'E': "falcon",
    'F': "quail",  # Note: The question's choices list has quail at position F, but we'll use the mapping from the problem
    'G': "hummingbird"
}

# Since we know the question asks for which bird is second from the right (position 6),
# and the problem states "The quail is the second from the right", we expect 'F' to be correct.
# But let's verify by checking which bird has position 6 in the solution.

solution = solutions[0]
for letter, bird_name in choices.items():
    if solution[bird_name] == 6:
        print(letter)
        break