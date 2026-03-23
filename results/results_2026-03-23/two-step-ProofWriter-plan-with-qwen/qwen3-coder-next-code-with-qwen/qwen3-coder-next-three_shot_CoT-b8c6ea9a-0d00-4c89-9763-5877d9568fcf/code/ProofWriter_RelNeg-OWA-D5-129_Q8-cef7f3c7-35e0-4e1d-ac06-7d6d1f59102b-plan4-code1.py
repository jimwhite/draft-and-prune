# --- Facts ---
facts:
is_cold("lion", True)
does_not_need("lion", "mouse", True)
visits("lion", "squirrel", True)

is_cold("mouse", True)
does_not_visit("mouse", "squirrel", True)

is_cold("rabbit", True)
is_rough("rabbit", True)
does_not_need("rabbit", "lion", True)
does_not_visit("rabbit", "squirrel", True)

is_kind("squirrel", True)
needs("squirrel", "mouse", True)
needs("squirrel", "rabbit", True)
does_not_see("squirrel", "lion", True)
does_not_see("squirrel", "rabbit", True)

# The rabbit does not see the mouse (implied - no statement says it does)
does_not_see("rabbit", "mouse", True)

# --- Rules ---
rules:
# If something needs the rabbit and the rabbit sees the mouse then the mouse does not see the lion.
foreach
    needs(?x, "rabbit")
    sees("rabbit", ?y)
assert
    does_not_see("mouse", "lion")

# If something is rough then it visits the mouse.
foreach
    is_rough(?x)
assert
    visits(?x, "mouse")

# If something needs the rabbit and it visits the mouse then the mouse needs the rabbit.
foreach
    needs(?x, "rabbit")
    visits(?x, "mouse")
assert
    needs("mouse", "rabbit")

# If something needs the rabbit and the rabbit is cold then it is rough.
foreach
    needs(?x, "rabbit")
    is_cold("rabbit")
assert
    is_rough(?x)

# If something needs the rabbit then the rabbit needs the squirrel.
foreach
    needs(?x, "rabbit")
assert
    needs("rabbit", "squirrel")

# If the squirrel sees the lion and the squirrel is not green then the lion needs the squirrel.
foreach
    sees("squirrel", "lion")
    not(is_green("squirrel"))
assert
    needs("lion", "squirrel")

# If something is big then it visits the lion.
foreach
    is_big(?x)
assert
    visits(?x, "lion")

# If something visits the squirrel and the squirrel sees the lion then the lion is not kind.
foreach
    visits(?x, "squirrel")
    sees("squirrel", "lion")
assert
    not(is_kind("lion"))

# --- Query ---
query:
does_not_need("mouse", "rabbit", False)