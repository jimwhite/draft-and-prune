from constraint import *

problem = Problem()

fruits = ["mangoes", "kiwis", "plums", "pears", "watermelons"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda kiwis, plums: kiwis < plums, ("kiwis", "plums"))

problem.addConstraint(lambda pears: pears == 3, ("pears",))

problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

solutions = problem.getSolutions()

for solution in solutions:
    if solution["pears"] == 3:
        print("D")
        break