# Facts
eats("bear", "squirrel")
is_cold("bear")
is_rough("bear")
visits("bear", "lion")

eats("cat", "lion")

likes("lion", "cat")
visits("lion", "bear")

eats("squirrel", "lion")
is_cold("squirrel")
is_rough("squirrel")
likes("squirrel", "bear")
visits("squirrel", "lion")

# Define all entities as persons
person("bear")
person("cat")
person("lion")
person("squirrel")

# Rules (using PyKe's foreach/then syntax)
def rule1():
    """If someone eats the lion then the lion is red."""
    foreach(eats(person, "lion"))
    assert(red("lion"))

def rule2():
    """If someone is green and they like the lion then they eat the bear."""
    foreach(green(person), likes(person, "lion"))
    assert(eats(person, "bear"))

def rule3():
    """If someone visits the bear then the bear likes the lion."""
    foreach(visits(person, "bear"))
    assert(likes("bear", "lion"))

def rule4():
    """If someone likes the squirrel and they like the lion then they visit the lion."""
    foreach(likes(person, "squirrel"), likes(person, "lion"))
    assert(visits(person, "lion"))

def rule5():
    """If someone is green then they eat the squirrel."""
    foreach(green(person))
    assert(eats(person, "squirrel"))

def rule6():
    """If someone likes the lion then they visit the bear."""
    foreach(likes(person, "lion"))
    assert(visits(person, "bear"))

def rule7():
    """If someone visits the lion and the lion is green then they are red."""
    foreach(visits(person, "lion"), green("lion"))
    assert(red(person))

def red_people_are_green():
    """Red people are green."""
    foreach(red(person))
    assert(green(person))

# Query: is the squirrel not rough?
# Since we know is_rough("squirrel") is true from facts, 
# the statement "squirrel is not rough" would be false
query_result = not is_rough("squirrel")