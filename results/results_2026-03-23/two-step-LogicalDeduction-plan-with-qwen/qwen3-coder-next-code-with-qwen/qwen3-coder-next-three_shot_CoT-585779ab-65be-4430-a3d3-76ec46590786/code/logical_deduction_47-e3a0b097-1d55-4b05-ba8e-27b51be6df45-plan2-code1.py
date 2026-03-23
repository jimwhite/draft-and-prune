from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["bluejay", "robin", "cardinal", "hawk", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The blue jay is the rightmost" → bluejay == 5
problem.addConstraint(lambda bluejay: bluejay == 5, ["bluejay"])

# 2. "The robin is to the right of the falcon" → falcon < robin
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# 3. "The cardinal is to the left of the hawk" → cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# 4. "The falcon is to the right of the hawk" → hawk < falcon
problem.addConstraint(lambda hawk, falcon: hawk < falcon, ["hawk", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Since the problem states the statements are consistent, there should be at least one solution
# The question asks which bird is rightmost (position 5)
# From constraint 1, bluejay must be at position 5, so choice A is true
# We can verify by checking the solution(s)
for solution in solutions:
    # Find which bird is at position 5
    for bird, pos in solution.items():
        if pos == 5:
            # The choices map to birds
            if bird == "bluejay":
                print("A")
            elif bird == "robin":
                print("B")
            elif bird == "cardinal":
                print("C")
            elif bird == "hawk":
                print("D")
            elif bird == "falcon":
                print("E")