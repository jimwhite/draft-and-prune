from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hummingbird", "cardinal", "blue jay", "owl", "raven", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hummingbird is to the left of the quail"
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ["hummingbird", "quail"])

# "The robin is to the left of the cardinal"
problem.addConstraint(lambda robin, cardinal: robin < cardinal, ["robin", "cardinal"])

# "The blue jay is the leftmost" (position 1)
problem.addConstraint(lambda blue_jay: blue_jay == 1, ["blue jay"])

# "The cardinal is the fourth from the left" (position 4)
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The raven is the third from the right" (position 5 in a 7-position sequence)
problem.addConstraint(lambda raven: raven == 5, ["raven"])

# "The owl is the third from the left" (position 3)
problem.addConstraint(lambda owl: owl == 3, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is leftmost (position 1)
# According to the constraints, blue jay must be at position 1
# Let's verify by checking the solution
for solution in solutions:
    # Find which bird is at position 1
    for bird, pos in solution.items():
        if pos == 1:
            # Map to the correct choice letter
            if bird == "blue jay":
                print("C")
            break