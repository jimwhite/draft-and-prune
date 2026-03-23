from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7, left to right)
birds = ["cardinal", "crow", "hummingbird", "bluejay", "owl", "robin", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The cardinal is to the right of the crow" → cardinal > crow
problem.addConstraint(lambda cardinal, crow: cardinal > crow, ("cardinal", "crow"))

# 2. "The quail is the third from the left" → quail == 3
problem.addConstraint(lambda quail: quail == 3, ("quail",))

# 3. "The owl is to the right of the robin" → owl > robin
problem.addConstraint(lambda owl, robin: owl > robin, ("owl", "robin"))

# 4. "The hummingbird is to the right of the blue jay" → hummingbird > bluejay
problem.addConstraint(lambda hummingbird, bluejay: hummingbird > bluejay, ("hummingbird", "bluejay"))

# 5. "The cardinal is the second from the left" → cardinal == 2
problem.addConstraint(lambda cardinal: cardinal == 2, ("cardinal",))

# 6. "The owl is the third from the right" → position = 7 - 3 + 1 = 5
problem.addConstraint(lambda owl: owl == 5, ("owl",))

# Solve the problem
solutions = problem.getSolutions()

# Since we know from constraint #5 that cardinal == 2, choice A is directly verified
# But to follow the plan precisely and confirm consistency:
for solution in solutions:
    # Check if cardinal is indeed at position 2 (as per constraint)
    if solution["cardinal"] == 2:
        print("A")
        break