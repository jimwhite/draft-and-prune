from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=most expensive, 5=least expensive)
fruits = ["loquats", "pears", "watermelons", "kiwis", "plums"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are the third-most expensive" → rank = 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# 3. "The loquats are more expensive than the watermelons" → loquats < watermelons
problem.addConstraint(lambda loquats, watermelons: loquats < watermelons, ["loquats", "watermelons"])

# 4. "The plums are less expensive than the watermelons" → plums > watermelons
problem.addConstraint(lambda watermelons, plums: watermelons < plums, ["watermelons", "plums"])

# 5. "The kiwis are more expensive than the pears" → kiwis < pears
problem.addConstraint(lambda kiwis, pears: kiwis < pears, ["kiwis", "pears"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names for second-most expensive (rank 2)
choices = {
    "A": "loquats",
    "B": "pears",
    "C": "watermelons",
    "D": "kiwis",
    "E": "plums"
}

# Find which fruit has rank 2 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)