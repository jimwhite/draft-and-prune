from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=most expensive, 5=cheapest)
fruits = ["pears", "mangoes", "kiwis", "oranges", "peaches"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are the most expensive" → rank(pears) = 1
problem.addConstraint(lambda pears: pears == 1, ["pears"])

# 3. "The peaches are more expensive than the mangoes" → rank(peaches) < rank(mangoes)
problem.addConstraint(lambda peaches, mangoes: peaches < mangoes, ["peaches", "mangoes"])

# 4. "The oranges are more expensive than the kiwis" → rank(oranges) < rank(kiwis)
problem.addConstraint(lambda oranges, kiwis: oranges < kiwis, ["oranges", "kiwis"])

# 5. "The mangoes are more expensive than the oranges" → rank(mangoes) < rank(oranges)
problem.addConstraint(lambda mangoes, oranges: mangoes < oranges, ["mangoes", "oranges"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks for the second-cheapest fruit (rank 4)
choices = {
    "A": "pears",
    "B": "mangoes",
    "C": "kiwis",
    "D": "oranges",
    "E": "peaches"
}

# Find which fruit has rank 4 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)