from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks: 1=most expensive, 3=least expensive)
fruits = ["apples", "pears", "loquats"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the loquats" -> pears rank < loquats rank
problem.addConstraint(lambda pears, loquats: pears < loquats, ("pears", "loquats"))

# 3. "The pears are less expensive than the apples" -> apples rank < pears rank
problem.addConstraint(lambda apples, pears: apples < pears, ("apples", "pears"))

# Find the solution
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "apples",
    "B": "pears",
    "C": "loquats"
}

# Find which fruit has rank 1 (most expensive) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)