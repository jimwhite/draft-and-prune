from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["apples", "mangoes", "oranges", "plums", "pears"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# The oranges are more expensive than the mangoes (oranges rank < mangoes rank)
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ("oranges", "mangoes"))

# The plums are the cheapest (plums rank = 1)
problem.addConstraint(lambda plums: plums == 1, ("plums",))

# The apples are less expensive than the mangoes (apples rank < mangoes rank)
problem.addConstraint(lambda apples, mangoes: apples < mangoes, ("apples", "mangoes"))

# The pears are more expensive than the oranges (pears rank < oranges rank)
problem.addConstraint(lambda pears, oranges: pears < oranges, ("pears", "oranges"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "apples",
    "B": "mangoes",
    "C": "oranges",
    "D": "plums",
    "E": "pears"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)