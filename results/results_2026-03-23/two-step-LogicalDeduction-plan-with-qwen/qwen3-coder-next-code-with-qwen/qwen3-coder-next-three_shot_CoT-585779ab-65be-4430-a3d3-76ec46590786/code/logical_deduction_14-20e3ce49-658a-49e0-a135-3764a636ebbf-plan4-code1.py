from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "kiwis", "plums", "pears", "watermelons"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the problem statements
# All fruits have different prices
problem.addConstraint(AllDifferentConstraint())

# Kiwis are less expensive than plums (kiwis < plums)
problem.addConstraint(lambda kiwis, plums: kiwis < plums, ["kiwis", "plums"])

# Pears are the third-most expensive (rank 3)
problem.addConstraint(lambda pears: pears == 3, ["pears"])

# Kiwis are the second-cheapest (rank 2)
problem.addConstraint(lambda kiwis: kiwis == 2, ["kiwis"])

# Watermelons are the most expensive (rank 5)
problem.addConstraint(lambda watermelons: watermelons == 5, ["watermelons"])

# Solve the problem
solutions = problem.getSolutions()

# Find which fruit has rank 3 (third-most expensive)
for solution in solutions:
    for choice, fruit in enumerate(["mangoes", "kiwis", "plums", "pears", "watermelons"], start=1):
        if solution[fruit] == 3:
            # Map to choice letters: A=1, B=2, C=3, D=4, E=5
            choice_letter = chr(ord('A') + choice - 1)
            print(choice_letter)