from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=cheapest, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are less expensive than the kiwis"
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ("watermelons", "kiwis"))

# "The kiwis are the second-most expensive"
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "mangoes",
    "B": "watermelons",
    "C": "kiwis"
}

# Find which fruit is the cheapest (rank 1)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)