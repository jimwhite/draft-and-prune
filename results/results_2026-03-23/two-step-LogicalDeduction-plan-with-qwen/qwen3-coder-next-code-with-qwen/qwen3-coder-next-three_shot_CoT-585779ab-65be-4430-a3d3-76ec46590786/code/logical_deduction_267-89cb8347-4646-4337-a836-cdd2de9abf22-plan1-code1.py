from constraint import *

problem = Problem()

fruits = ["kiwis", "oranges", "watermelons"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda kiwis, oranges: kiwis < oranges, ("kiwis", "oranges"))

problem.addConstraint(lambda oranges, watermelons: oranges < watermelons, ("oranges", "watermelons"))

solutions = problem.getSolutions()

choices = {
    "A": "kiwis",
    "B": "oranges",
    "C": "watermelons"
}

for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)