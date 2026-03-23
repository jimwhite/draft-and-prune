from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["mangoes", "kiwis", "plums", "pears", "watermelons"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The kiwis are less expensive than the plums" → kiwis < plums
problem.addConstraint(lambda kiwis, plums: kiwis < plums, ("kiwis", "plums"))

# 3. "The pears are the third-most expensive" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# 4. "The kiwis are the second-cheapest" → kiwis == 2
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# 5. "The watermelons are the most expensive" → watermelons == 5
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# Solve for the arrangement
solutions = problem.getSolutions()

# The question asks which fruit is third-most expensive (rank 3)
# From the constraints, we already know pears == 3, but let's verify with the solution
for solution in solutions:
    # Check which fruit has rank 3 and match to choices
    if solution["mangoes"] == 3:
        print("A")
    elif solution["kiwis"] == 3:
        print("B")
    elif solution["plums"] == 3:
        print("C")
    elif solution["pears"] == 3:
        print("D")
    elif solution["watermelons"] == 3:
        print("E")