from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The pears are more expensive than the kiwis" → kiwis < pears
problem.addConstraint(lambda kiwis, pears: kiwis < pears, ("kiwis", "pears"))

# 2. "The watermelons are less expensive than the peaches" → watermelons < peaches
problem.addConstraint(lambda watermelons, peaches: watermelons < peaches, ("watermelons", "peaches"))

# 3. "The mangoes are the third-cheapest" → mangoes == 3
problem.addConstraint(lambda mangoes: mangoes == 3, ("mangoes",))

# 4. "The watermelons are the third-most expensive" → rank = 5 (since 7-3+1=5)
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# 5. "The plums are the second-most expensive" → rank = 6 (since 7-2+1=6)
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# 6. "The loquats are the second-cheapest" → loquats == 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Find which fruit has rank 3 (third-cheapest)
for solution in solutions:
    for fruit, rank in solution.items():
        if rank == 3:
            # Map to the correct choice letter
            fruit_to_choice = {
                "loquats": "A",
                "peaches": "B",
                "watermelons": "C",
                "plums": "D",
                "kiwis": "E",
                "mangoes": "F",
                "pears": "G"
            }
            print(fruit_to_choice[fruit])