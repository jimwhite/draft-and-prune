from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["robin", "hummingbird", "raven", "bluejay", "crow", "cardinal", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The hummingbird is to the left of the crow."
problem.addConstraint(lambda h, c: h < c, ("hummingbird", "crow"))

# 2. "The cardinal is to the right of the quail."
problem.addConstraint(lambda q, ca: q < ca, ("quail", "cardinal"))

# 3. "The blue jay is the fourth from the left."
problem.addConstraint(lambda b: b == 4, ("bluejay",))

# 4. "The robin is the second from the left."
problem.addConstraint(lambda r: r == 2, ("robin",))

# 5. "The quail is to the right of the crow."
problem.addConstraint(lambda c, q: c < q, ("crow", "quail"))

# 6. "The raven is to the left of the robin."
problem.addConstraint(lambda rv, r: rv < r, ("raven", "robin"))

# Solve the problem
solutions = problem.getSolutions()

# Since the problem is well-defined, there should be exactly one solution
solution = solutions[0]

# The question asks which statement is true, and choice A directly states
# "The robin is the second from the left", which we have as a constraint (robin == 2)
# So A must be true. We can verify it holds in the solution.
assert solution["robin"] == 2, "Inconsistent solution: robin is not at position 2"

# Output the correct choice
print("A")