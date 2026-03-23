from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=least expensive, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The kiwis are the second-most expensive"
problem.addConstraint(lambda kiwis: kiwis == 2, ["kiwis"])

# "The watermelons are less expensive than the kiwis"
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Determine the correct answer by checking which choice matches the solution
for solution in solutions:
    # Check each choice
    if solution["mangoes"] == 2:
        print("A")
    elif solution["watermelons"] == 2:
        print("B")
    elif solution["kiwis"] == 2:
        print("C")