from constraint import *

problem = Problem()

vehicles = ["tractor", "truck", "minivan"]
ranks = range(1, 4)
problem.addVariables(vehicles, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda truck, minivan: truck < minivan, ("truck", "minivan"))

problem.addConstraint(lambda tractor, truck: tractor < truck, ("tractor", "truck"))

solutions = problem.getSolutions()

for solution in solutions:
    if solution["tractor"] == 1:
        print("A")
    elif solution["truck"] == 1:
        print("B")
    elif solution["minivan"] == 1:
        print("C")