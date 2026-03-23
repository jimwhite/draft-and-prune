from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "kiwis", "plums", "pears", "watermelons"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The kiwis are less expensive than the plums" -> kiwis < plums
problem.addConstraint(lambda kiwis, plums: kiwis < plums, ("kiwis", "plums"))

# "The pears are the third-most expensive" -> pears == 3
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# "The kiwis are the second-cheapest" -> kiwis == 2
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# "The watermelons are the most expensive" -> watermelons == 5
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "plums",
    "D": "pears",
    "E": "watermelons"
}

# Find which fruit is most expensive (rank 5) and print corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)