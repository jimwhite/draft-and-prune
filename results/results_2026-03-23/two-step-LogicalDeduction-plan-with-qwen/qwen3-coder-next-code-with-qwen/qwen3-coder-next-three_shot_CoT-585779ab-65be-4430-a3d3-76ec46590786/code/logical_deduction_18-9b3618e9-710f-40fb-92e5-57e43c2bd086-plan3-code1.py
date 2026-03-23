from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["hawk", "raven", "robin", "hummingbird", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The robin is the leftmost" → robin == 1
problem.addConstraint(lambda robin: robin == 1, ["robin"])

# "The raven is the second from the left" → raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The hawk is the second from the right" → hawk == 4
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# "The crow is the third from the left" → crow == 3
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Since we have 5 birds and 4 fixed positions, hummingbird must be in position 5
# But we don't need to compute it explicitly for this question

# The question asks which statement is true
# Choice A: "The hawk is the second from the right." → This corresponds to hawk == 4, which we enforced
# All other choices contradict the constraints (e.g., raven is second from left, not right)

# We can verify by checking the solution
for solution in solutions:
    # Check which choice matches a true statement
    if solution["hawk"] == 4:  # hawk is second from right (position 4)
        print("A")
    elif solution["raven"] == 4:  # raven is second from right
        print("B")
    elif solution["robin"] == 4:  # robin is second from right
        print("C")
    elif solution["hummingbird"] == 4:  # hummingbird is second from right
        print("D")
    elif solution["crow"] == 4:  # crow is second from right
        print("E")