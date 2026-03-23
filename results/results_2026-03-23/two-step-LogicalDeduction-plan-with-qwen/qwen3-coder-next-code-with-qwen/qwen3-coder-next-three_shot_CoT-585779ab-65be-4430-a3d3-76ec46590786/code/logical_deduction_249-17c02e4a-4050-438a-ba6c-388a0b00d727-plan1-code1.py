from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 3, where 1 = first place)
golfers = ["ana", "rob", "joe"]
ranks = range(1, 4)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers must have different ranks
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana → joe < ana
# Rob finished above Joe → rob < joe
# Combined: rob < joe < ana
problem.addConstraint(lambda rob, joe, ana: rob < joe and joe < ana, ["rob", "joe", "ana"])

# Solve the problem
solutions = problem.getSolutions()

# Determine who finished second (rank = 2)
for solution in solutions:
    if solution["ana"] == 2:
        print("A")
    elif solution["rob"] == 2:
        print("B")
    elif solution["joe"] == 2:
        print("C")