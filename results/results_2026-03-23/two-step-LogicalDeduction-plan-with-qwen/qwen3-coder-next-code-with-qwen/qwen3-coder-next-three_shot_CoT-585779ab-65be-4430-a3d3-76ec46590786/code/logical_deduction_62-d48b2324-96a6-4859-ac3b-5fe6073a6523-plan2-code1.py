from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["mangoes", "kiwis", "plums", "pears", "watermelons"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# Kiwis are less expensive than plums (kiwis < plums)
problem.addConstraint(lambda kiwis, plums: kiwis < plums, ("kiwis", "plums"))

# Pears are the third-most expensive (rank 3)
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# Kiwis are the second-cheapest (rank 2)
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Watermelons are the most expensive (rank 5)
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "plums",
    "D": "pears",
    "E": "watermelons"
}

# Find which fruit has rank 5 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)