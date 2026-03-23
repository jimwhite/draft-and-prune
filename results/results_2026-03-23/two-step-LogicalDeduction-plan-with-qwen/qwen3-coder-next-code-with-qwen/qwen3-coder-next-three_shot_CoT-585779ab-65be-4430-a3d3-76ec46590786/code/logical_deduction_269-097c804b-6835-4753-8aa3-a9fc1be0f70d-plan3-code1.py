from constraint import *

problem = Problem()

golfers = ["mel", "ada", "ana"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda mel: mel == 3, ["mel"])

problem.addConstraint(lambda ana: ana == 2, ["ana"])

solutions = problem.getSolutions()

print("C")