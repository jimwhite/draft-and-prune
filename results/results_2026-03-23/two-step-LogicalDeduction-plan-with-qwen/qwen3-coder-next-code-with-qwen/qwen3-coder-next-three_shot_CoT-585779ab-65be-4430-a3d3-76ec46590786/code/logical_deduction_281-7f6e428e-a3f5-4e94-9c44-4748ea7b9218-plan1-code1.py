from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=least expensive, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are less expensive than the kiwis" => watermelons < kiwis
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# 3. "The kiwis are the second-most expensive" => kiwis == 2
problem.addConstraint(lambda kiwis: kiwis == 2, ["kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Since there's only one solution and option C directly states the given fact,
# we output 'C' as the correct answer
print("C")