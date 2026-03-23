from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1=cheapest to 7=most expensive)
fruits = ["kiwis", "plums", "mangoes", "watermelons", "pears", "peaches", "oranges"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferentConstraint to ensure unique price ranks
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The pears are the third-cheapest" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ["pears"])

# 2. "The kiwis are the second-most expensive" → kiwis == 6
problem.addConstraint(lambda kiwis: kiwis == 6, ["kiwis"])

# 3. "The pears are more expensive than the plums" → plums < pears (plums < 3)
problem.addConstraint(lambda plums, pears: plums < pears, ["plums", "pears"])

# 4. "The oranges are less expensive than the kiwis" → oranges > kiwis (oranges > 6)
problem.addConstraint(lambda oranges, kiwis: oranges > kiwis, ["oranges", "kiwis"])

# 5. "The mangoes are the third-most expensive" → mangoes == 5
problem.addConstraint(lambda mangoes: mangoes == 5, ["mangoes"])

# 6. "The peaches are the second-cheapest" → peaches == 2
problem.addConstraint(lambda peaches: peaches == 2, ["peaches"])

# Solve the problem
solutions = problem.getSolutions()

# Find which fruit has rank 1 (cheapest)
for solution in solutions:
    for fruit, rank in solution.items():
        if rank == 1:
            cheapest_fruit = fruit
            break

# Map choice letters to fruits
choices = {
    "A": "kiwis",
    "B": "plums",
    "C": "mangoes",
    "D": "watermelons",
    "E": "pears",
    "F": "peaches",
    "G": "oranges"
}

# Find and print the corresponding choice letter
for letter, fruit in choices.items():
    if fruit == cheapest_fruit:
        print(letter)