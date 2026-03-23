from constraint import *

problem = Problem()

vehicles = ["convertible", "sedan", "tractor", "minivan", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda tractor, minivan: tractor > minivan, ("tractor", "minivan"))

problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

problem.addConstraint(lambda convertible, sedan: convertible < sedan, ("convertible", "sedan"))

problem.addConstraint(lambda convertible: convertible == 4, ("convertible",))

solutions = problem.getSolutions()

for solution in solutions:
    if solution["convertible"] == 4:
        print("A")
        break