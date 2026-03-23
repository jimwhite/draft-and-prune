from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["mangoes", "kiwis", "oranges", "watermelons", "apples", "pears", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the oranges" → loquats < oranges
problem.addConstraint(lambda loquats, oranges: loquats < oranges, ("loquats", "oranges"))

# 3. "The oranges are the third-most expensive" → rank = 7 - 3 + 1 = 5
problem.addConstraint(lambda oranges: oranges == 5, ("oranges",))

# 4. "The apples are the cheapest" → rank = 1
problem.addConstraint(lambda apples: apples == 1, ("apples",))

# 5. "The kiwis are more expensive than the pears" → kiwis > pears
problem.addConstraint(lambda kiwis, pears: kiwis > pears, ("kiwis", "pears"))

# 6. "The mangoes are more expensive than the watermelons" → mangoes > watermelons
problem.addConstraint(lambda mangoes, watermelons: mangoes > watermelons, ("mangoes", "watermelons"))

# 7. "The loquats are more expensive than the kiwis" → loquats > kiwis
problem.addConstraint(lambda loquats, kiwis: loquats > kiwis, ("loquats", "kiwis"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "oranges",
    "D": "watermelons",
    "E": "apples",
    "F": "pears",
    "G": "loquats"
}

# Find the fruit with rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)