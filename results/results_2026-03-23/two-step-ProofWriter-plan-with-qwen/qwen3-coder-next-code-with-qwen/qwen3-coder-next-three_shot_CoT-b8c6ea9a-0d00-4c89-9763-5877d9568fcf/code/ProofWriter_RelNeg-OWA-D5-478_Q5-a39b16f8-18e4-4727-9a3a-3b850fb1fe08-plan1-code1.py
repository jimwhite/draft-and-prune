# Facts
facts:
    is_kind("cow", True)
    sees("cow", "mouse", True)
    eats("mouse", "cow", True)
    is_kind("mouse", True)
    needs("mouse", "squirrel", True)
    eats("rabbit", "mouse", True)
    is_not_blue("rabbit", True)
    is_not_blue("squirrel", True)
    is_green("squirrel", True)
    is_rough("squirrel", True)
    needs("squirrel", "mouse", True)
    sees("squirrel", "rabbit", True)

# Rules
rules:
    # Rule 1: If something sees the cow then it sees the squirrel
    rule1:
        if sees(?x, "cow", True)
        then sees(?x, "squirrel", True)

    # Rule 2: If something sees the rabbit then it eats the cow
    rule2:
        if sees(?x, "rabbit", True)
        then eats(?x, "cow", True)

    # Rule 3: If something needs the cow then the cow eats the mouse
    rule3:
        if needs(?x, "cow", True)
        then eats("cow", "mouse", True)

    # Rule 4: If something needs the squirrel and the squirrel needs the cow then the cow does not need the rabbit
    rule4:
        if needs(?x, "squirrel", True) and needs("squirrel", "cow", True)
        then not needs("cow", "rabbit", True)

    # Rule 5: If the mouse eats the rabbit and the rabbit does not see the mouse then the rabbit is green
    rule5:
        if eats("mouse", "rabbit", True) and not sees("rabbit", "mouse", True)
        then is_green("rabbit", True)

    # Rule 6: If the cow needs the rabbit then the rabbit does not eat the mouse
    rule6:
        if needs("cow", "rabbit", True)
        then not eats("rabbit", "mouse", True)

    # Rule 7: If something eats the squirrel and the squirrel eats the cow then it needs the cow
    rule7:
        if eats(?x, "squirrel", True) and eats("squirrel", "cow", True)
        then needs(?x, "cow", True)

    # Rule 8: If something eats the mouse then it eats the squirrel
    rule8:
        if eats(?x, "mouse", True)
        then eats(?x, "squirrel", True)

# Query
query:
    needs("rabbit", "cow", True)