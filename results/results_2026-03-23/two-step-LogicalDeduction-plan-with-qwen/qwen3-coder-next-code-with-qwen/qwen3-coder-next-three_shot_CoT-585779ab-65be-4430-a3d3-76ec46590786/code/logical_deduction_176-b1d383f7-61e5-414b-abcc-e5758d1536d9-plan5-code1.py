from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["plums", "kiwis", "pears", "mangoes", "apples", "oranges", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The pears are less expensive than the oranges" → pears < oranges
problem.addConstraint(lambda pears, oranges: pears < oranges, ("pears", "oranges"))

# 2. "The mangoes are less expensive than the kiwis" → mangoes < kiwis
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ("mangoes", "kiwis"))

# 3. "The plums are the second-most expensive" → plums rank = 6 (since 7 is most expensive)
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# 4. "The loquats are more expensive than the apples" → loquats < apples
problem.addConstraint(lambda loquats, apples: loquats < apples, ("loquats", "apples"))

# 5. "The kiwis are less expensive than the apples" → kiwis < apples
problem.addConstraint(lambda kiwis, apples: kiwis < apples, ("kiwis", "apples"))

# 6. "The loquats are the fourth-most expensive" → loquats rank = 4
problem.addConstraint(lambda loquats: loquats == 4, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "plums",
    "B": "kiwis",
    "C": "pears",
    "D": "mangoes",
    "E": "apples",
    "F": "oranges",
    "G": "loquats"
}

# Find the fruit with rank 3 (third-cheapest) and print corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)