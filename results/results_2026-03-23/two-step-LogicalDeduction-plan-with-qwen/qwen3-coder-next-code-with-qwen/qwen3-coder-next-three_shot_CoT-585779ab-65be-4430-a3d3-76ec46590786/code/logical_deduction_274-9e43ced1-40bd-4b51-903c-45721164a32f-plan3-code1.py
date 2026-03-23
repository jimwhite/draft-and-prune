from constraint import *

problem = Problem()

fruits = ["peaches", "pears", "mangoes"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

problem.addConstraint(lambda peaches: peaches == 1, ("peaches",))

solutions = problem.getSolutions()

print("A")