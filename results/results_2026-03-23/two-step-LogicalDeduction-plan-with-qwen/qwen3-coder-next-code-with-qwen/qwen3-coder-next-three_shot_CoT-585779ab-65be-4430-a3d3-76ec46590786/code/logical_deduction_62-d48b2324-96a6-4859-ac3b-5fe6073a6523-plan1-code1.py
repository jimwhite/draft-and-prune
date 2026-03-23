from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "kiwis", "plums", "pears", "watermelons"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the problem statements
# All fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# Kiwis are less expensive than plums: kiwis < plums
problem.addConstraint(lambda kiwis, plums: kiwis < plums, ("kiwis", "plums"))

# Pears are the third-most expensive: pears == 3
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# Kiwis are the second-cheapest: kiwis == 2
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Watermelons are the most expensive: watermelons == 5
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which fruit is most expensive (rank 5)
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "plums",
    "D": "pears",
    "E": "watermelons"
}

# Find the fruit with rank 5 and print its corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)