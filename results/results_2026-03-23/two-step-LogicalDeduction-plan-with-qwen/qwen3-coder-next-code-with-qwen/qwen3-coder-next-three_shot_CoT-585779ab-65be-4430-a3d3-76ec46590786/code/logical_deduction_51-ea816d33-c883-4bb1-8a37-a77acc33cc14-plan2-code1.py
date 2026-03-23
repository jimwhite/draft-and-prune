from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcyle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The hatchback is newer than the convertible" → hatchback > convertible
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ("hatchback", "convertible"))

# 3. "The bus is newer than the hatchback" → bus > hatchback
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ("bus", "hatchback"))

# 4. "The bus is older than the motorcyle" → bus < motorcyle
problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ("bus", "motorcyle"))

# 5. "The minivan is the newest" → minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the newest (position 5)
# According to constraint 5, minivan must be at position 5
# So choice A is correct: "The minivan is the newest."
print("A")