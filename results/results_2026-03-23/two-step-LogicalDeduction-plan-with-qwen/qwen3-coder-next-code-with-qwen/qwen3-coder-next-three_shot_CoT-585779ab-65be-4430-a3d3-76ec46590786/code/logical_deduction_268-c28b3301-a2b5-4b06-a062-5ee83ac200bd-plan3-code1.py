from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=cheapest, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are less expensive than the kiwis"
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# "The kiwis are the second-most expensive"
problem.addConstraint(lambda kiwis: kiwis == 2, ["kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which fruit is cheapest (rank 1)
for solution in solutions:
    if solution["mangoes"] == 1:
        print("A")
    elif solution["watermelons"] == 1:
        print("B")
    elif solution["kiwis"] == 1:
        print("C")