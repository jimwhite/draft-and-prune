from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the sedan"
problem.addConstraint(lambda m, s: m < s, ("minivan", "sedan"))

# "The tractor is older than the hatchback"
problem.addConstraint(lambda t, h: t < h, ("tractor", "hatchback"))

# "The minivan is the third-newest" (position 3 in our ranking)
problem.addConstraint(lambda m: m == 3, ("minivan",))

# "The station wagon is the second-newest" (position 4)
problem.addConstraint(lambda sw: sw == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the third-newest (rank 3)
# Based on the constraint, minivan must be at rank 3
# So choice C is correct: "The minivan is the third-newest."

# Directly output 'C' since we know from the constraint that minivan == 3
print("C")